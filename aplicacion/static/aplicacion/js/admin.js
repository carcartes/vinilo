
    // Datos de ejemplo para los gráficos
    const ventasData = {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
        datasets: [{
            label: 'Ventas Mensuales',
            data: [100, 200, 300, 400, 500, 600],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    };
    const usuariosData = {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
        datasets: [{
            label: 'Registros de Usuarios',
            data: [50, 100, 150, 200, 250, 300],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    };

    // Configuración de los gráficos
    const chartOptions = {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    // Inicializar gráficos
    const ventasChart = new Chart(document.getElementById('ventas-chart'), {
        type: 'bar',
        data: ventasData,
        options: chartOptions
    });

    const usuariosChart = new Chart(document.getElementById('usuarios-chart'), {
        type: 'line',
        data: usuariosData,
        options: chartOptions
    });
    