import os
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

from contextcheck.generators.endpoint_wrapper import RagApiWrapperBase
from contextcheck.loaders.yaml import load_yaml_file


class DocumentQuestions(BaseModel):
    model_config = ConfigDict(extra="ignore")

    document: str = Field(description="A document from which a question is derived?")
    questions: list[str] = Field(description="A list of questions regarding a document")


class AnswerGenerator(BaseModel):
    top_k: int = 3
    collection_name: str = "default"
    questions_file: Path
    api_wrapper: RagApiWrapperBase
    questions: list[DocumentQuestions] = Field(
        default_factory=list, description="A list of nested questions regarding a document"
    )
    alpha: float = 0.75
    use_ranker: bool = True
    debug: bool = False

    def model_post_init(self, __context):
        questions_dict = load_yaml_file(self.questions_file)["questions"]
        self.questions = TypeAdapter(list[DocumentQuestions]).validate_python(questions_dict)

    def generate(self) -> dict:
        """
        Generate answers for the given questions.

        Returns:
            dict: A dictionary containing the questions and their answers.
        """

        qa_data = {"QA": []}

        for document_questions in self.questions:
            current_document = document_questions.document
            entry = {"document": current_document, "qa": []}
            list_of_questions = document_questions.questions
            print("Generating answers for document:", current_document)
            for idx, question in enumerate(list_of_questions):
                answer = self.api_wrapper.query_qa(
                    question, use_ranker=self.use_ranker, top_k=self.top_k, alpha=self.alpha
                )
                qa_item = {
                    "question": question,
                    "answer": answer["result"],
                }

                if self.debug:
                    qa_item["chunks_and_documents"] = [
                        [
                            {
                                "chunk": answer["chunk"],
                                "document": answer["metadata"]["document_name"],
                            }
                        ]
                        for answer in answer.get("relevant_documents", {}).get(
                            "collection_retriever_entries", []
                        )
                    ]

                print(f"Processing {idx + 1}/{len(list_of_questions)} questions")
                entry["qa"].append(qa_item)
            qa_data["QA"].append(entry)

        return qa_data

    def save_to_yaml(self, filepath: str):
        """
        Save the generated questions to a YAML file.

        Args:
            filepath (str): The path to the output file.

        Returns:
            None
        """
        qa = self.generate()
        dirs = os.path.dirname(filepath)
        if dirs:
            os.makedirs(dirs, exist_ok=True)

        with open(filepath, "w") as f:
            yaml.dump(qa, stream=f, width=200)
