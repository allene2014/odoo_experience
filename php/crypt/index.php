<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RestClient</title>
    <link rel="stylesheet" href="css/estilo.css" type="text/css">
</head>
<body>

<div  class="container">
    <h1>Api para Encriptar/Des-encriptar</h1>
    <div class="divbody">
        <h3>Encrypt</h3>
        <code>
           POST  /encrypt
           <br>
           {
               <br>
               "cvv"    : "",   -> REQUERIDO
               <br>
               "keybank": ""    -> REQUERIDO
               <br>
            }
        
        </code>
    </div>      
    <div class="divbody">   
        <h3>Decrypt</h3>
        <code>
           POST  /decrypt
           <br>
           {
               <br>
               "cvvencrypt" : "",  -> REQUERIDO
               <br>
               "keybank"    : ""   -> REQUERIDO
               <br>
            }
        
        </code>
    </div>


</div>
    
</body>
</html>
