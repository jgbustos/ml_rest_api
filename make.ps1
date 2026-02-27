$StyleOn="$($PSStyle.Bold)$($PSStyle.Foreground.Blue)"
$StyleOff="$($PSStyle.Reset)"
Write-Host $StyleOn"---------- Reformating with black... ----------"$StyleOff
black .\ml_rest_api .\tests
Write-Host $StyleOn"---------- Analysing with pylint... -----------"$StyleOff
pylint --recursive=y .\ml_rest_api .\tests
Write-Host $StyleOn"---------- Validating with mypy... ------------"$StyleOff
mypy --pretty --config-file=mypy.ini .\ml_rest_api
