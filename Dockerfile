FROM python:3.9-slim

ENV DISCORD_TOKEN=CHANGETHIS
ENV HOME_ASSISTANT_URL=https://example.com
ENV HOME ASSISTANT_TOKEN=CHANGETHIS
ENV USER_ID=CHANGETHIS

WORKDIR /app

RUN pip install discord.py requests --quiet

RUN useradd app
USER app

COPY main.py ./main.py

CMD ["python3", "main.py"]