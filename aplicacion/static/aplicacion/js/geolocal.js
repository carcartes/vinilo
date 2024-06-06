// Solicitud al punto final público de ipapi para obtener datos de geolocalización
$.get("https://ipapi.co/json/")
    .done(function (data) {
        if (data) {
            const country = data.country_name;
            const region = data.region;
            const city = data.city;
            const latitude = data.latitude;
            const longitude = data.longitude;

            $("#location").text(`País: ${country}, Región: ${region}, Ciudad: ${city}, Latitud: ${latitude}, Longitud: ${longitude}`);
        } else {
            $("#location").text("No se pudo obtener la ubicación.");
        }
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
        console.error("Error al obtener la ubicación:", errorThrown);
        $("#location").text("Error al obtener la ubicación.");
    });