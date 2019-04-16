FROM pamamu/s2t_main-controller

ARG SHARED_FOLDER
ENV SHARED_FOLDER = $SHARED_FOLDER
ARG SPEECH2TEXT_NAME
ENV SPEECH2TEXT_NAME = $SPEECH2TEXT_NAME

WORKDIR /srv/S2T/S2T_Speech2Text

ADD . .

RUN apk add --update pulseaudio-dev alsa-lib-dev
RUN pip install -r requirements.txt

CMD python src/app.py $SPEECH2TEXT_NAME $SHARED_FOLDER


