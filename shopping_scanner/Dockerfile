ARG BUILD_FROM
FROM $BUILD_FROM
RUN apk add --no-cache python3
COPY proxy_server.py /proxy_server.py
COPY rootfs /
RUN chmod a+x /etc/services.d/webserver/run
RUN chmod a+x /proxy_server.py
EXPOSE 8099
LABEL io.hass.name="Shopping Scanner" \
    io.hass.description="Barcode scanner for shopping lists" \
    io.hass.type="addon" \
    io.hass.version="1.0.6" \
    maintainer="Simon Weaver <simon@nrg-music.co.uk>"