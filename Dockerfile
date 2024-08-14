FROM docker.io/library/python:alpine AS build

LABEL "org.opencontainers.image.source" = "https://codeberg.org/ahmubashshir/anime-game-daily-login-helper"
LABEL "maintainer" = "Mubashshir <ahmubashshir@gmail.com>"

WORKDIR /build

COPY an_anime_game_check_in an_anime_game_check_in
COPY poetry.lock pyproject.toml .

RUN python3 -m venv venv
ENV PATH="/build/venv/bin:$PATH"
ENV HOME=/build

RUN pip --no-cache-dir --disable-pip-version-check --no-input install build
RUN python3 -m build
RUN rm -rf venv

FROM docker.io/library/python:alpine
COPY --from=build /build/dist /dist
RUN pip --no-cache-dir --disable-pip-version-check --no-input \
	install --root-user-action=ignore dist/*.whl && rm -rf /dist

ENTRYPOINT ["an-anime-game-check-in"]
