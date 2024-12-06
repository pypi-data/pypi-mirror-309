from pathlib import Path
from typing import List

from pymultirole_plugins.v1.schema import Document, DocumentList
from starlette.datastructures import UploadFile

from pyconverters_xcago.xcago import (
    XCagoConverter,
    XCagoParameters,
)


def test_xcago_json():
    converter = XCagoConverter()
    parameters = XCagoParameters()
    testdir = Path(__file__).parent
    source = Path(testdir, "data/dpv-stern_20241113_highres_article_72-1.json_")
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "	application/json"), parameters
        )
        assert len(docs) == 1
        assert docs[0].identifier == 'dpv-stern_20241113_highres_article_72-1'
        dl = DocumentList(__root__=docs)
        result = Path(testdir, "data/dpv-stern_20241113_highres_article_72-1.json")
        with result.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
