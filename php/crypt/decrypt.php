<?php
    header('Access-Control-Allow-Origin: *');
    header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");
    header("Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, PATCH, DELETE");
    header("Allow: GET, POST, OPTIONS, PUT, PATCH, DELETE");
    $method = $_SERVER['REQUEST_METHOD'];
    if($method == "OPTIONS") {
        die();
    }

    require_once 'clases/respuestas.class.php';
    require_once 'clases/encript.class.php';

    $_AesCipher = new AesCipher;
    $_respuestas = new respuestas;

    if($_SERVER['REQUEST_METHOD'] == 'POST') {
        // Recibimos el dato
        $postBody = file_get_contents("php://input");
        $datos = json_decode($postBody, true);

        // Validamos los campos
        if(!isset($datos["cvvencrypt"]) || !isset($datos["keybank"])) {
            $respuesta = $_respuestas->error_400();
        } else {
            $cvvencrypt = mb_convert_encoding($datos["cvvencrypt"], "UTF-8");
            $keybank = mb_convert_encoding($datos["keybank"], "UTF-8");
    
            $keyhash = $_AesCipher->createKeyhash($keybank);
            $decrypted = $_AesCipher->decrypt($keyhash,$cvvencrypt);

            $respuesta = array(
                "CVVEncriptado" => $cvvencrypt,
                "CVVDes-Encriptado" => $decrypted
            );
        }
        header('Content-Type: application/json');
        die(json_encode($respuesta));
    }



?>