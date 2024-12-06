import json
from langchain.vectorstores import Chroma
# from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.embeddings import Embeddings


from langchain.docstore.document import Document

from langchain.document_loaders import DataFrameLoader

from langchain.text_splitter import TextSplitter
import numpy as np

# from langchain_community.document_loaders.hugging_face_dataset import HuggingFaceDatasetLoader
from ddi_fw.langchain.embeddings import SBertEmbeddings
from ddi_fw.utils import get_import


def load_configuration(config_file):
    """
    Load the configuration from a JSON file.
    """
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def split_dataframe(df, min_size=512, max_size=1024):
    # Ensure the total size of the DataFrame is larger than the desired split size
    total_size = len(df)
    
    # Check if the dataframe is large enough
    if total_size <= min_size:
       return df
    
    # List to store partial DataFrames
    partial_dfs = []

    # Start splitting the DataFrame
    start_idx = 0
    
    while start_idx < total_size:
        # Calculate the size of the next chunk: it should be between min_size and max_size
        chunk_size = np.random.randint(min_size, max_size + 1)
        
        # Ensure that the chunk size does not exceed the remaining data
        chunk_size = min(chunk_size, total_size - start_idx)
        
        # Create the partial DataFrame and append to the list
        partial_dfs.append(df.iloc[start_idx:start_idx + chunk_size])
        
        # Update the start index for the next chunk
        start_idx += chunk_size
    
    return partial_dfs

class DataFrameToVectorDB:
    def __init__(self,
                 collection_name,
                 persist_directory,
                 embeddings: Embeddings,
                 text_splitter: TextSplitter,
                 batch_size=1000):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embeddings = embeddings
        self.text_splitter = text_splitter
        self.batch_size = batch_size  # to store chunks partially
        self.vectordb = Chroma(collection_name=collection_name,
                               persist_directory=persist_directory,
                               embedding_function=embeddings)

    def __split_docs(self, documents):
        docs = self.text_splitter.split_documents(documents)
        return docs

    def __split_list(self, input_list, batch_size):
        for i in range(0, len(input_list), batch_size):
            yield input_list[i:i + batch_size]

    def store_documents(self, df, columns, page_content_columns):
        """
        Core function that processes the documents and adds them to the vector database.
        """
        for page_content_column in page_content_columns:
            copy_columns = columns.copy()
            copy_columns.append(page_content_column)
            col_df = df[copy_columns].copy()
            col_df.dropna(subset=[page_content_column], inplace=True)
            col_df['type'] = page_content_column  # Set the type column
            documents = []

            loader = DataFrameLoader(
                data_frame=col_df, page_content_column=page_content_column)
            loaded_docs = loader.load()
            documents.extend(self.__split_docs(loaded_docs))

            split_docs_chunked = self.__split_list(documents, self.batch_size)

            for split_docs_chunk in split_docs_chunked:
                # vectordb = Chroma.from_documents(
                #     collection_name=collection_name,
                #     documents=split_docs_chunk,
                #     embedding=embeddings,
                #     persist_directory=persist_directory,
                # )
                self.vectordb.add_documents(split_docs_chunk)
                self.vectordb.persist()

    def store(self, df, columns, page_content_columns, partial_df_size=None):
        """
        Store function to handle both full and partial dataframe processing.
        """
        if partial_df_size:
            partial_dfs  = split_dataframe(df, min_size = partial_df_size)
            for partial_df in partial_dfs:
                self.store_documents(df=partial_df, columns=columns,
                                     page_content_columns=page_content_columns)
            # Process the dataframe in chunks if partial_df_size is provided
            # for i in range(0, len(df), partial_df_size):
            #     batch = df[i: i + partial_df_size]
            #     self.store_documents(df=batch, columns=columns,
            #                          page_content_columns=page_content_columns)
        else:
            # Process the entire dataframe if no partial_df_size is specified
            self.store_documents(df=df, columns=columns,
                                 page_content_columns=page_content_columns)


def generate_embeddings(df, config_file, new_model_names, collections=None, persist_directory="embeddings"):
    """
    Generate embeddings for collections based on a configuration file.

    collections: List of collections that contain metadata for embedding generation.
    config_file: Path to the configuration file containing model settings.
    new_model_names: List of model names to generate embeddings for.
    """
    # Load the configuration from the provided file
    if not collections:
        collections = load_configuration(config_file)

    # Process each collection
    for collection_config in collections:
        id = collection_config['id']
        name = collection_config['name']

        # Skip if the collection's name is not in the list of new model names
        if name not in new_model_names:
            continue

        # # Find the matching configuration for the collection
        # collection_config = next(
        #     (item for item in collections if item['id'] == id), None)

        # if not collection_config:
        #     print(f"Configuration for collection {id} not found.")
        #     continue

        embedding_model_type = collection_config['embedding_model_type']
        text_splitters_types = collection_config['text_splitters_types']
        batch_size = collection_config['batch_size']
        columns = collection_config['columns']
        page_content_columns = collection_config['page_content_columns']
        persist_directory = f'{persist_directory}/{id}'

        # Load the embedding model and text splitter dynamically
        print(f"Generating embeddings for {id} with model {name}...")

        # Assuming the classes for the embeddings and splitters are available
        try:
            model_kwargs = collection_config['model_kwargs']
            SBertEmbeddings(model_name="a", model_config={})
            model = get_import(embedding_model_type)(
                model_name=name, **model_kwargs)
        except:
            # print(f"Unknown embedding model: {embedding_model_type}")
            raise Exception(f"Unknown embedding model: {embedding_model_type}")

        text_splitters = []
        text_splitters_suffixes = []
        for text_splitter_type in text_splitters_types:
            try:
                type_of_text_splitter = get_import(text_splitter_type.get("type"))
                kwargs = text_splitter_type.get("params")
                suffix = text_splitter_type.get("suffix")
                if kwargs:
                    text_splitter = type_of_text_splitter(
                        **kwargs)
                else:
                    text_splitter = type_of_text_splitter()
                text_splitters.append(text_splitter)
                text_splitters_suffixes.append(suffix)
            except:
                print(f"Unknown text splitter: {text_splitter_type}")
                raise Exception(f"Unknown text splitter: {text_splitter_type}")

        for text_splitter, suffix in zip(text_splitters, text_splitters_suffixes):
            print(f"{id}_{suffix}")
            to_vector_db = DataFrameToVectorDB(collection_name=f"{id}_{suffix}",
                                               persist_directory=persist_directory,
                                               embeddings=model,
                                               text_splitter=text_splitter,
                                               batch_size=1024)
            to_vector_db.store(
                df, columns, page_content_columns, partial_df_size=batch_size)
