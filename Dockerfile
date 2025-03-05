FROM python:3.14.0a5
WORKDIR /app

ENV DISCORD_TOKEN=CHANGETHIS
ENV HOME_ASSISTANT_URL=https://example.com
ENV HOME_ASSISTANT_TOKEN=CHANGETHIS
ENV USER_ID=CHANGETHIS

RUN pip install discord.py requests

RUN useradd app
USER app

COPY main.py ./main.py

CMD ["python3", "main.py"]  