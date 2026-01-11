ARG BUILD_FROM
FROM $BUILD_FROM
RUN apk add --no-cache nginx
COPY rootfs /
RUN chmod a+x /etc/services.d/nginx/run
EXPOSE 8099
LABEL io.hass.name="Shopping Scanner" \
    io.hass.description="Barcode scanner for shopping lists" \
    io.hass.type="addon" \
    io.hass.version="1.0.0" \
    maintainer="Simon Weaver <simon@nrg-music.co.uk>"