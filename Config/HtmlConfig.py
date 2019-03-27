# TODO : def getNavbar(postBody):

alertHtmlBef = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Alert</title>
<style>
        body{
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgb(98, 98, 98);
        }
        .card{
            width: 400px;
            height: 400px;
            direction: rtl;
            text-align: center;
            background: white;
            border-radius: 50%;
            box-shadow: 0 0 1px 2px rgba(255, 255, 255, 0.1);
            transition: 0.5s;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            animation: anim 3s linear infinite;
        }
        @keyframes anim {
            0% {
                background: #eb8585;
                width: 400px;
            height: 400px;
            }
            50% {
                background: #f36060;
                width: 500px;
                height: 500px;
            }
            100% {
                width: 400px;
                height: 400px;
                background :  #eb8585;
            }
        }
        .card:hover{
            box-shadow: 0px 0px 8px 10px rgba(255, 255, 255, 0.1);
        }
        .msg{
            direction: rtl;
            color: rgb(78, 64, 64);
            background: white;
            padding: 10px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="card">
        <p class="msg">
'''
alertHtmlAfter = '''
        </p>
    </div>
</body>
</html>'''


def getAlertHtml(msg):
    return alertHtmlBef + msg + alertHtmlAfter