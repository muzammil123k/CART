Write-Host "🚀 Flipping 100% of live traffic to the Green environment..." -ForegroundColor Green

& "C:\Program Files\Amazon\AWSCLIV2\aws.exe" elbv2 modify-listener `
    --listener-arn "arn:aws:elasticloadbalancing:us-east-1:972553756445:listener/app/CART-Production-ALB/4ea08299239ec53d/465164341840526a" `
    --default-actions "Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:972553756445:targetgroup/CART-TG-Green/0e11a1afa5a9652b" `
    --no-cli-pager

Write-Host "✅ Cutover complete. Green is now live!" -ForegroundColor Cyan