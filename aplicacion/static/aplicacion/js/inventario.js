document.addEventListener('DOMContentLoaded', function () {
    // Funcionalidad para eliminar productos
    document.querySelectorAll('.btn-eliminar').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.closest('tr').remove();
        });
    });

    // Funcionalidad para editar productos y cargar datos en el formulario de edición
    document.querySelectorAll('.btn-editar').forEach(btn => {
        btn.addEventListener('click', () => {
            const fila = btn.closest('tr');
            const nombreProducto = fila.querySelector('td:nth-child(2)').innerText;
            const descripcionProducto = fila.querySelector('td:nth-child(3)').innerText;
            const precioProducto = fila.querySelector('td:nth-child(4)').innerText.replace('$', '');
            const stockProducto = fila.querySelector('td:nth-child(5)').innerText;

            document.getElementById('nombreProductoEditar').value = nombreProducto;
            document.getElementById('descripcionProductoEditar').value = descripcionProducto;
            document.getElementById('precioProductoEditar').value = precioProducto;
            document.getElementById('stockProductoEditar').value = stockProducto;

            document.getElementById('formularioEditarProducto').setAttribute('data-id-producto', fila.dataset.idProducto);
        });
    });

    // Guardar cambios en el formulario de edición con validación
    document.getElementById('guardarCambios').addEventListener('click', () => {
        const form = document.getElementById('formularioEditarProducto');

        // Verificar si el formulario es válido
        if (form.checkValidity()) {
            const idProducto = document.getElementById('formularioEditarProducto').getAttribute('data-id-producto');
            const nombreProducto = document.getElementById('nombreProductoEditar').value;
            const descripcionProducto = document.getElementById('descripcionProductoEditar').value;
            const precioProducto = document.getElementById('precioProductoEditar').value;
            const stockProducto = document.getElementById('stockProductoEditar').value;

            const fila = document.querySelector(`tr[data-id-producto="${idProducto}"]`);
            fila.querySelector('td:nth-child(2)').innerText = nombreProducto;
            fila.querySelector('td:nth-child(3)').innerText = descripcionProducto;
            fila.querySelector('td:nth-child(4)').innerText = `$${precioProducto}`;
            fila.querySelector('td:nth-child(5)').innerText = stockProducto;

            // Cerrar el modal solo si el formulario es válido
            const modal = bootstrap.Modal.getInstance(document.getElementById('editarProductoModal'));
            modal.hide();
        } else {
            // Mostrar la validación si el formulario no es válido
            form.classList.add('was-validated');
        }
    });

    // Funcionalidad para agregar productos con validación
    document.getElementById('agregarNuevoProducto').addEventListener('click', () => {
        const form = document.getElementById('formularioAgregarProducto');

        // Verificar si el formulario es válido
        if (form.checkValidity()) {
            const nombreProducto = document.getElementById('nombreProductoNuevo').value;
            const descripcionProducto = document.getElementById('descripcionProductoNuevo').value;
            const precioProducto = document.getElementById('precioProductoNuevo').value;
            const stockProducto = document.getElementById('stockProductoNuevo').value;

            const tbody = document.querySelector('table tbody');
            const nuevaFila = document.createElement('tr');
            const nuevoId = tbody.children.length + 1;

            nuevaFila.setAttribute('data-id-producto', nuevoId);
            nuevaFila.innerHTML = `
                <td>${nuevoId}</td>
                <td>${nombreProducto}</td>
                <td>${descripcionProducto}</td>
                <td>$${precioProducto}</td>
                <td>${stockProducto}</td>
                <td>
                    <button class="btn btn-danger btn-eliminar"><i class="far fa-trash-alt"></i> Eliminar</button>
                    <button class="btn btn-primary btn-editar" data-bs-toggle="modal" data-bs-target="#editarProductoModal"><i class="far fa-edit"></i> Editar</button>
                </td>
            `;

            tbody.appendChild(nuevaFila);

            const modal = bootstrap.Modal.getInstance(document.getElementById('agregarProductoModal'));
            modal.hide();

            // Actualizar eventos para nuevos botones de eliminar y editar
            actualizarEventos();
        } else {
            // Mostrar la validación si el formulario no es válido
            form.classList.add('was-validated');
        }
    });

    function actualizarEventos() {
        document.queryselectorAll('.btn-editar').forEach(btn => {
            btn.addEventListener('click', () => {
                const fila = btn.closest('tr');
                const nombreProducto = fila.querySelector('td:nth-child(2)').innerText;
                const descripcionProducto = fila.querySelector('td:nth-child(3)').innerText;
                const precioProducto = fila.querySelector('td:nth-child(4)').innerText.replace('$', '');
                const stockProducto = fila.querySelector('td:nth-child(5)').innerText;

                document.getElementById('nombreProductoEditar').value = nombreProducto;
                document.getElementById('descripcionProductoEditar').value;
                document.getElementById('precioProductoEditar').value;
                document.getElementById('stockProductoEditar').value;

                document.getElementById('formularioEditarProducto').setAttribute('data-id-producto', fila.dataset.idProducto);
            });
        });

        document.queryselectorAll('.btn-eliminar').forEach(btn => {
            btn.addEventListener('click', () => {
                btn.closest('tr').remove();
            });
        });
    }

    // Inicializar eventos por primera vez
    actualizarEventos();
});