Write-Host "🚨 Emergency Rollback: Flipping traffic back to stable Blue..." -ForegroundColor Red

& "C:\Program Files\Amazon\AWSCLIV2\aws.exe" elbv2 modify-listener `
    --listener-arn "arn:aws:elasticloadbalancing:us-east-1:972553756445:listener/app/CART-Production-ALB/4ea08299239ec53d/465164341840526a" `
    --default-actions "Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:972553756445:targetgroup/CART-TG-Blue/819b9b46f70712f6" `
    --no-cli-pager

Write-Host "🔄 Rollback complete. Blue is back live!" -ForegroundColor Cyan