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
            background: rgb(248, 117, 117);
        }
        .card{
            width: 60%;
            height: 30vh;
            direction: rtl;
            text-align: center;
            background: white;
            border-radius: 8px;
            padding-top: 50px;
            padding-bottom: 50px;
            box-shadow: 0 0 1px 2px rgba(0, 0, 0, 0.1);
            transition: 0.5s;
        }
        .card:hover{
            box-shadow: 0px 0px 8px 10px rgba(0, 0, 0, 0.1);
        }
        .msg{
            direction: rtl;
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