CREATE TABLE stupidity_table
(
    rated  BIGSERIAL   NOT NULL,
    rater  BIGSERIAL   NOT NULL,
    rating SMALLSERIAL NOT NULL
);

CREATE TABLE users
(
    id               BIGSERIAL PRIMARY KEY NOT NULL,
    username         TEXT                  NOT NULL,
    discriminator    SMALLSERIAL           NOT NULL,
    avatar_url       TEXT                  NOT NULL,
    token            TEXT UNIQUE           NOT NULL,
    token_expires_at TIMESTAMP             NOT NULL,
    renew_token      TEXT UNIQUE           NOT NULL
);

-- This is so that other clients of the same user don't get left behind. They can get the
-- Latest token (not expired) with an expired token.
CREATE TABLE token_history
(
    token TEXT PRIMARY KEY NOT NULL,
    id    BIGSERIAL        NOT NULL
);
