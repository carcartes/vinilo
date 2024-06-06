
document.addEventListener('DOMContentLoaded', function () {
    // Botón Eliminar Pedido
    document.querySelectorAll('.btn-eliminar').forEach(btn => {
        btn.addEventListener('click', () => {
            // Eliminar el pedido de la interfaz
            btn.closest('tr').remove();
        });
    });

    // Botón Editar Pedido
    document.querySelectorAll('.btn-editar').forEach(btn => {
        btn.addEventListener('click', () => {
            // Obtener los datos del pedido de la fila seleccionada
            const fila = btn.closest('tr');
            const estadoPedido = fila.querySelector('td:nth-child(5)').innerText.trim();

            // Llenar el formulario de edición con los datos del pedido
            document.getElementById('estadoPedido').value = estadoPedido;

            // Almacenar el ID del pedido en un atributo de datos del formulario
            document.getElementById('formularioEditarPedido').setAttribute('data-id-pedido', fila.dataset.idPedido);
        });
    });

    // Botón Guardar cambios del pedido
    document.getElementById('guardarCambiosPedido').addEventListener('click', () => {
        // Obtener el ID del pedido del formulario
        const idPedido = document.getElementById('formularioEditarPedido').getAttribute('data-id-pedido');

        // Obtener el nuevo estado del pedido del formulario
        const estadoPedido = document.getElementById('estadoPedido').value;
        let estadoBadge;
        switch (estadoPedido) {
            case '1':
                estadoBadge = '<span class="badge bg-danger">En proceso</span>';
                break;
            case '2':
                estadoBadge = '<span class="badge bg-warning text-dark">En camino</span>';
                break;
            case '3':
                estadoBadge = '<span class="badge bg-success">Entregado</span>';
                break;
            case '4':
                estadoBadge = '<span class="badge bg-secondary">Cancelado</span>';
                break;
            default:
                estadoBadge = '';
        }

        // Actualizar el estado del pedido en la fila correspondiente
        const fila = document.querySelector(`tr[data-id-pedido="${idPedido}"]`);
        fila.querySelector('td:nth-child(5)').innerHTML = estadoBadge;

        // Cerrar el modal de edición
        const modal = bootstrap.Modal.getInstance(document.getElementById('editarPedidoModal'));
        modal.hide();
    });
});