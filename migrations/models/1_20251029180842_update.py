from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "diaries" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "diaries" DROP COLUMN "updated_at";"""


MODELS_STATE = (
    "eJztW1tz2joQ/isMT+lM22lJepnzRgg5TdtAm7iXaSbjEbYCGmzJ2HITpsN/P5KwLcu3E1"
    "NIbKI3WO3a2k/S7qeV/KfrEhs6wctjQuYu8Ofdfzp/uhi4kP3ItT3vdIHnyRYuoGDiCOVJ"
    "pCWkYBJQH1iUNdwAJ4BMZMPA8pFHEcFMikPH4UJiMUWEp1IUYrQIoUnJFNIZ9FnD1TUTI2"
    "zDOxjEf725eYOgYyv9RTZ/t5CbdOkJ2Rmmp0KRv21iWsQJXSyVvSWdEZxoI0y5dAox9AGF"
    "/PHUD3n3ee8iV2OP1j2VKusupmxseANCh6bcvScGFsEcP9abQDg45W950Xt99O7o/eHbo/"
    "dMRfQkkbxbrd2Tvq8NBQIjo7sS7YCCtYaAUeJm+ZA7awKax++EtVDkwmIQVcsMmHZk+jL+"
    "kYU2BrIK21ggwZUTakvoMh/sMXaW0cBVQGmcnQ8vjf75F+6JGwQLR0DUN4a8pSeky4z04O"
    "0zLidsOawXSvKQzo8z40OH/+38Go+GAkES0Kkv3ij1jF9d3icQUmJicmsCOzXHYmkMDNOU"
    "A7sICYVmrWWRNvn/xbHZCDZyeUjUwgD69UBLWTwhzHgcvpkXRhQOSB6/U+JDNMWf4FLAeM"
    "Z6BLAFC2CLMs+36DGNg28Vz4BYKl/hg9skNaUnBvOO+QSp8G/Qvxz0T4bd/GrdAmpf4+e0"
    "FrZ0ECrGjc+9CbDmt8C3TWUS8hbSIxlJoptvcntuVgIwmAr/uRu80xGyJwj4yyKKtG6o5E"
    "c2U0FQs6NGhrIqdkQRdQqW5WAG/GLsEoMMfKzTDWVALrgzHYindMb+vn71qgKv7/2LwYf+"
    "xQHTyvCaUdTUW7epOZW9kUJcwC8NeFcyBVMmbQGyijoOfxoKa4zhOjjv/3ymMMfP49G/sX"
    "oK3sHn8XEWVU3c95O4h5694cCqlnpgH3Vgo87rrYXeWjz81uJxKPLXEAaRyzmWnLRVEuVF"
    "pKWpciOXZhVVjofOpIzV1eF6OUPN+CTjywXD8pWdyTTKUlLH4jiyP/10AR0Qr8ryWJleu4"
    "0dhlzQXO021BERcgviXFSAqQpyTEVHuNZFOL2P3cU+llHmGSlgdeU1FmmxEabRrGt/jWWj"
    "3KAc1W6eFtLnwo2dww+bEgwyh/jYYc9yUECLckNGozJJUK5rThRlnS1alC3EANYqHccGbc"
    "kUaljrvXlzj7DGtErDmmhTkwO885C/US1MtdxCLezh00ZLSl+x29VFTV380sWvvS5+CVwL"
    "kn6Md3mq5w7p7WAjl2NVgufDJn7XyPFpm+2k+Z2jqCT5w/tsXQ7Ldy6HucNhDwTBLWGLbw"
    "aCWR0oc4aaNkna5ALk1AEzMXjaO2p9vr53x7D6fH1PBzap5+gSWK0SWHoppO4lbo5Dcv+x"
    "pSBkKm1/iUa+xtdSWPQh4s4rxgosJVvH+92byA/WdveSV0n1YZHqT4roXOvd5o4PHzUd3Q"
    "fWUvSdVnT9peanWorVE6qQ6qqyrio//tdaMgn+JXDbpUWP9s2WEo2aVJbvQx9ZsyJ2FbVU"
    "8iogdXRtvmFBrYot/YZ+ULg+y0ugKRNdSZa3s9jSqAFipN5OAB/247ePl+NR3UuD3zBz8M"
    "pGFn3e4eWF62bCWoEi91oh5rkrhNnbghnGzR9Q82L09tPL6j+ZP1Ks"
)
