from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "questions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "question_text" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "quotes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "author" VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(30) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "email" VARCHAR(100),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "bookmarks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "quote_id" INT NOT NULL REFERENCES "quotes" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_bookmarks_quote_i_107863" ON "bookmarks" ("quote_id");
CREATE INDEX IF NOT EXISTS "idx_bookmarks_user_id_a8e8e3" ON "bookmarks" ("user_id");
CREATE TABLE IF NOT EXISTS "diaries" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_diaries_user_id_12cb33" ON "diaries" ("user_id");
CREATE TABLE IF NOT EXISTS "token_blacklist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(255) NOT NULL,
    "expired_at" TIMESTAMPTZ,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_token_black_user_id_4fd74a" ON "token_blacklist" ("user_id");
CREATE TABLE IF NOT EXISTS "user_questions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "question_id" INT NOT NULL REFERENCES "questions" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_user_questi_user_id_c633d7" UNIQUE ("user_id", "question_id", "created_at")
);
CREATE INDEX IF NOT EXISTS "idx_user_questi_questio_3a19a1" ON "user_questions" ("question_id");
CREATE INDEX IF NOT EXISTS "idx_user_questi_user_id_505e01" ON "user_questions" ("user_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztW21zmzgQ/isef0pn0k7rpG3mvjmOc03b2NeE3nWayTAyKLbGIGEQl3g6/u8nyYAQbx"
    "ccO4Fa3+zVLmgfsbuPFvGr6xIbOsGbU0LmLvDn3T86v7oYuJD9yI0ddrrA8+QIF1AwcYTy"
    "JNISUjAJqA8sygbugBNAJrJhYPnIo4hgJsWh43AhsZgiwlMpCjFahNCkZArpDPps4OaWiR"
    "G24QMM4r/e3LxD0LGV+SKb31vITbr0hOwC03OhyO82MS3ihC6Wyt6SzghOtBGmXDqFGPqA"
    "Qn556od8+nx2kauxR+uZSpX1FFM2NrwDoUNT7j4SA4tgjh+bTSAcnPK7vO69O/54fHL04f"
    "iEqYiZJJKPq7V70ve1oUBgZHRXYhxQsNYQMErcLB9yZ01A8/idsRGKXFgMomqZAdOOTN/E"
    "P7LQxkBWYRsLJLjygdoSuswHe4ydZbRwFVAaF5fDa6N/+Rf3xA2ChSMg6htDPtIT0mVGev"
    "DhFZcTFg7rQEku0vnnwvjU4X87P8ejoUCQBHTqiztKPeNnl88JhJSYmNybwE49Y7E0BoZp"
    "yoVdhIRCs1ZYpE3+Pzg2W8FGhodELQygXw+0lMUeYcbz8N28MKNwQPL4nRMfoin+ApcCxg"
    "s2I4AtWABbVHm+R5dpHHyr+AmIpfIWPrhPSlP6wWDeMZ8gFf4N+teD/tmwm4/WLaD2Lb5O"
    "a2FLJ6Fi3PizNwHW/B74tqk8hHyE9EhGkujmh9yem5UADKbCf+4Gn3SE7BkC/rKIIq0HKv"
    "mRzVQQ1Oyokamsih1RRJ2CsBzMgF+MXWKQgY9NuqEMyAUPpgPxlM7Y33dv31bg9Xf/avCp"
    "f3XAtDK8ZhQN9dZjak1ld6QQF/BLAz6UPIIpk7YAWUUdhz8MhTXGcB1c9n+8Upjj1/Hoz1"
    "g9Be/g6/g0i6om7r8ncdcUVFPQ56KgL0OlvoUwiFzOsalkrJJQLSItTakaGZpVlCpeOpOy"
    "6l+HE+QMNTOQzCCXDMsjO1NplFBS1+I0sj//cgUdEEdlea5Mx25jlyGXNFe7TXVEpNyCPB"
    "dt1KuSHFPRGa51GU7vd3ax32GceUYKWF35XlxabIRp9NS1fy++UW1QXultXhbS7w8b+ww/"
    "b0kwyBziU4ddy0EBLaoNGY3KIkG5rjlRlHW1aFG1EAtYq8UYG7SlUqhprff+/SPSGtMqTW"
    "tiTC0O8MFD/kbNMNVyC82w5y8bLel9xW7r5pdufu1x80vgWlD0Y7zLSz13SG8HGxmOVQWe"
    "L5v4XaPGp222U+Z3jqJS5I8es3U5Kt+5HOVeInogCO4JC74ZCGZ1oMwZatokaZMLkFMHzM"
    "Rgv3fU+j3sPryH9ewNF1a11Av7ogub9HN0C6xWCywdCqnza5vjkJyTaykImU7bE9HI9/ha"
    "Cot+ibjzjrECS8nW8XHnJvKLtd295E3SfVik5pMiOrd6t7njl4+ajv4OrKXoe57o+EvNT3"
    "oUqz3qkOqusu4qv/xXPbIIPhG47dKiF/u2R8lGTWrL96GPrFkRu4pGKnkVkDq6N9+wpFbF"
    "lv6FflAYn+Ut0JSJ7iTL01ksNGqAGKm3E8Dn/Ujq8/V4VPfQ4HfMHLyxkUUPO7y9cNtMWC"
    "tQ5F4rxDx3hDB7WjDDuPkFah6M3n55Wf0Hi+m7eQ=="
)
