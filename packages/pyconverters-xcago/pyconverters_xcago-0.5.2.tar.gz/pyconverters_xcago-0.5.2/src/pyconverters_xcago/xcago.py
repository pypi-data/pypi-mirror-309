import json
import logging
import os
from typing import List, Type

from pydantic import BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile

_home = os.path.expanduser("~")


class XCagoParameters(ConverterParameters):
    pass


logger = logging.getLogger("pymultirole")


class XCagoConverter(ConverterBase):
    """XCago converter ."""

    def convert(
            self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:
        docs = []
        try:
            jdoc = json.load(source.file)
            lang = jdoc['source']['language_code']
            metadata = {
                'language': lang,
                'date': jdoc['source']['date'],
                'date_created': jdoc['source']['date_created'],
                'country_code': jdoc['source']['country_code'],
                'byline': jdoc['byline']
            }
            doc = Document(identifier=jdoc['local_id'], title=jdoc['headline'], text=jdoc[
                'story'], metadata=metadata)
            doc.metadata['original'] = source.filename
            docs.append(doc)
        except BaseException as err:
            logger.warning(
                f"Cannot parse document {source.filename}",
                exc_info=True,
            )
            raise err
        return docs

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return XCagoParameters
