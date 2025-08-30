<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

try {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $input_data = file_get_contents('php://input');
        $input = json_decode($input_data, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new Exception('Error al decodificar JSON: ' . json_last_error_msg());
        }
        
        echo json_encode([
            'status' => 'test_success',
            'input' => $input,
            'method' => $_SERVER['REQUEST_METHOD'],
            'timestamp' => date('c')
        ], JSON_UNESCAPED_UNICODE);
        
    } else {
        echo json_encode([
            'status' => 'error',
            'message' => 'Use POST con JSON',
            'method' => $_SERVER['REQUEST_METHOD']
        ], JSON_UNESCAPED_UNICODE);
    }
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'status' => 'error',
        'message' => 'Error interno: ' . $e->getMessage(),
        'timestamp' => date('c')
    ], JSON_UNESCAPED_UNICODE);
}
?>
