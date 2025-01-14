from typing import List

from langchain.schema import BaseRetriever
from langchain_community.vectorstores import PGVector

from langflow.custom import Component
from langflow.helpers.data import docs_to_data
from langflow.io import BoolInput, HandleInput, IntInput, Output, StrInput
from langflow.schema import Data


class PGVectorStoreComponent(Component):
    display_name = "PGVector"
    description = "PGVector Vector Store with search capabilities"
    documentation = "https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/pgvector"
    icon = "PGVector"

    inputs = [
        StrInput(name="pg_server_url", display_name="PostgreSQL Server Connection String", required=True),
        StrInput(name="collection_name", display_name="Table", required=True),
        HandleInput(name="embedding", display_name="Embedding", input_types=["Embeddings"]),
        HandleInput(
            name="vector_store_inputs",
            display_name="Vector Store Inputs",
            input_types=["Document", "Data"],
            is_list=True,
        ),
        BoolInput(
            name="add_to_vector_store",
            display_name="Add to Vector Store",
            info="If true, the Vector Store Inputs will be added to the Vector Store.",
        ),
        StrInput(name="search_input", display_name="Search Input"),
        IntInput(
            name="number_of_results",
            display_name="Number of Results",
            info="Number of results to return.",
            value=4,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Vector Store", name="vector_store", method="build_vector_store", output_type=PGVector),
        Output(
            display_name="Base Retriever",
            name="base_retriever",
            method="build_base_retriever",
            output_type=BaseRetriever,
        ),
        Output(display_name="Search Results", name="search_results", method="search_documents"),
    ]

    def build_vector_store(self) -> PGVector:
        return self._build_pgvector()

    def _build_pgvector(self) -> PGVector:
        if self.add_to_vector_store:
            documents = []
            for _input in self.vector_store_inputs or []:
                if isinstance(_input, Data):
                    documents.append(_input.to_lc_document())
                else:
                    documents.append(_input)

            if documents:
                pgvector = PGVector.from_documents(
                    embedding=self.embedding,
                    documents=documents,
                    collection_name=self.collection_name,
                    connection_string=self.pg_server_url,
                )
            else:
                pgvector = PGVector.from_existing_index(
                    embedding=self.embedding,
                    collection_name=self.collection_name,
                    connection_string=self.pg_server_url,
                )
        else:
            pgvector = PGVector.from_existing_index(
                embedding=self.embedding,
                collection_name=self.collection_name,
                connection_string=self.pg_server_url,
            )

        return pgvector

    def search_documents(self) -> List[Data]:
        vector_store = self._build_pgvector()

        if self.search_input and isinstance(self.search_input, str) and self.search_input.strip():
            docs = vector_store.similarity_search(
                query=self.search_input,
                k=self.number_of_results,
            )

            data = docs_to_data(docs)
            self.status = data
            return data
        else:
            return []
