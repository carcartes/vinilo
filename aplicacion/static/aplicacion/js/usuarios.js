document.addEventListener("DOMContentLoaded", function () {
    const agregarUsuarioButton = document.getElementById("agregarNuevoUsuario");
    const formularioAgregarUsuario = document.getElementById("formularioAgregarUsuario");

    const guardarCambiosUsuarioButton = document.getElementById("guardarCambiosUsuario");
    const formularioEditarUsuario = document.getElementById("formularioEditarUsuario");

    const editarModal = new bootstrap.Modal(document.getElementById("editarUsuarioModal"));

    function validarFormulario(formulario) {
        if (!formulario.checkValidity()) {
            formulario.classList.add("was-validated");
            return false;
        }
        formulario.classList.remove("was-validated");
        return true;
    }

    function togglePasswordVisibility(event) {
        const button = event.currentTarget;
        const inputId = button.getAttribute("data-target");
        const input = document.querySelector(inputId);
        const icon = button.querySelector("i");

        if (input.type === "password") {
            input.type = "text";
            icon.classList.replace("fa-eye", "fa-eye-slash"); // Cambia el ícono para indicar que se está mostrando
        } else {
            input.type = "password";
            icon.classList.replace("fa-eye-slash", "fa-eye"); // Cambia el ícono para indicar que se está ocultando
        }
    }

    document.querySelectorAll(".toggle-password").forEach((button) => {
        button.addEventListener("click", togglePasswordVisibility);
    });

    function agregarUsuario() {
        if (!validarFormulario(formularioAgregarUsuario)) {
            return;
        }

        const nombre = document.getElementById("nombreNuevoUsuario").value;
        const apellido = document.getElementById("apellidoNuevoUsuario").value;
        const email = document.getElementById("emailNuevoUsuario").value;
        const telefono = document.getElementById("telefonoNuevoUsuario").value;
        const rut = document.getElementById("rutNuevoUsuario").value;
        const contrasena = document.getElementById("contrasenaNuevoUsuario").value;

        const tableBody = document.querySelector("tbody");
        const nuevaFila = document.createElement("tr");
        const nuevaId = tableBody.children.length + 1;

        nuevaFila.setAttribute("data-id-usuario", nuevaId);
        nuevaFila.innerHTML = `
            <td>${nuevaId}</td>
            <td>${nombre}</td>
            <td>${apellido}</td>
            <td>${email}</td>
            <td>${telefono}</td>
            <td>${rut}</td>
            <td>********</td> <!-- Contraseña oculta -->
            <td>
                <button class="btn btn-danger btn-eliminar">Eliminar</button>
                <button class="btn btn-primary btn-editar" data-bs-toggle="modal" data-bs-target="#editarUsuarioModal">Editar</button>
            </td>
        `;

        tableBody.appendChild(nuevaFila);

        formularioAgregarUsuario.reset();
        const modalAgregar = bootstrap.Modal.getInstance(document.getElementById("agregarUsuarioModal"));
        modalAgregar.hide();

        actualizarEventosEditarYEliminar(); // Vuelve a asignar los eventos para las nuevas filas
    }

    function guardarCambiosUsuario() {
        if (!validarFormulario(formularioEditarUsuario)) {
            return;
        }

        const idUsuario = document.getElementById("idUsuario").value;
        const nombre = document.getElementById("nombreUsuario").value;
        const apellido = document.getElementById("apellidoUsuario").value;
        const email = document.getElementById("emailUsuario").value;
        const telefono = document.getElementById("telefonoUsuario").value;
        const rut = document.getElementById("rutUsuario").value;
        const contrasena = document.getElementById("contrasenaUsuario").value;

        const fila = document.querySelector(`tr[data-id-usuario='${idUsuario}']`);

        fila.children[1].innerText = nombre;
        fila.children[2].innerText = apellido;
        fila.children[3].innerText = email;
        fila.children[4].innerText = telefono;
        fila.children[5].innerText = rut;
        fila.children[6].innerText = "********"; // Mantener la contraseña oculta en la tabla

        editarModal.hide(); // Cierra el modal de edición
    }

    agregarUsuarioButton.addEventListener("click", agregarUsuario);
    guardarCambiosUsuarioButton.addEventListener("click", guardarCambiosUsuario);

    function btnEliminarEventHandler(event) {
        const btn = event.currentTarget;
        const fila = btn.closest("tr");
        fila.remove();
    }

    function btnEditarEventHandler(event) {
        const btn = event.currentTarget;
        const fila = btn.closest("tr");

        const idUsuario = fila.getAttribute("data-id-usuario");
        const nombre = fila.children[1].innerText;
        const apellido = fila.children[2].innerText;
        const email = fila.children[3].innerText;
        const telefono = fila.children[4].innerText;
        const rut = fila.children[5].innerText;

        // Al editar, el campo de contraseña queda vacío para que el usuario lo reescriba si lo desea.
        document.getElementById("idUsuario").value = idUsuario;
        document.getElementById("nombreUsuario").value = nombre;
        document.getElementById("apellidoUsuario").value = apellido;
        document.getElementById("emailUsuario").value = email;
        document.getElementById("telefonoUsuario").value = telefono;
        document.getElementById("rutUsuario").value = rut;
        document.getElementById("contrasenaUsuario").value = "";

        editarModal.show(); // Muestra el modal de edición
    }

    function actualizarEventosEditarYEliminar() {
        document.querySelectorAll(".btn-eliminar").forEach((btn) => {
            btn.removeEventListener("click", btnEliminarEventHandler);
            btn.addEventListener("click", btnEliminarEventHandler);
        });

        document.querySelectorAll(".btn-editar").forEach((btn) => {
            btn.removeEventListener("click", btnEditarEventHandler);
            btn.addEventListener("click", btnEditarEventHandler);
        });
    }

    actualizarEventosEditarYEliminar(); // Asigna eventos para las nuevas filas
});