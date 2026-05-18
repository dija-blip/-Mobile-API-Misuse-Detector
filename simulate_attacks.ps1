# simulate_attacks.ps1
# Simulates all attack types to trigger both rule-based AND ML detection
# Run: .\simulate_attacks.ps1

$base = "http://localhost:8000/analyze"
$h = @{ "Content-Type" = "application/json" }

function Send($body) {
    try {
        $r = Invoke-RestMethod -Uri $base -Method POST -Headers $h -Body $body
        return $r
    } catch { return $null }
}

# ─────────────────────────────────────────────
# 1. BRUTEFORCE — triggers: failed_auth_ratio, login_attempts
# ─────────────────────────────────────────────
Write-Host "`n[1] BRUTEFORCE — 10.0.0.10" -ForegroundColor Red
for ($i = 1; $i -le 20; $i++) {
    $r = Send '{"ip":"10.0.0.10","method":"POST","endpoint":"/login","status_code":401,"response_time_ms":120,"user_agent":"python-requests/2.28","country":"RU"}'
    if ($i % 5 -eq 0) { Write-Host "  req=$i score=$($r.risk_score) level=$($r.risk_level) ai=$($r.ai_score) attack=$($r.attack_type)" }
}

# ─────────────────────────────────────────────
# 2. BURST — triggers: requests_per_minute > threshold
# ─────────────────────────────────────────────
Write-Host "`n[2] BURST — 10.0.0.11" -ForegroundColor Yellow
for ($i = 1; $i -le 50; $i++) {
    $r = Send '{"ip":"10.0.0.11","method":"GET","endpoint":"/api/products","status_code":200,"response_time_ms":30,"user_agent":"curl/7.68","country":"CN"}'
    if ($i % 10 -eq 0) { Write-Host "  req=$i score=$($r.risk_score) level=$($r.risk_level) ai=$($r.ai_score) attack=$($r.attack_type)" }
}

# ─────────────────────────────────────────────
# 3. ENDPOINT HAMMERING — triggers: unique_endpoints <= 2
# ─────────────────────────────────────────────
Write-Host "`n[3] ENDPOINT HAMMERING — 10.0.0.12" -ForegroundColor Cyan
for ($i = 1; $i -le 60; $i++) {
    $r = Send '{"ip":"10.0.0.12","method":"GET","endpoint":"/api/search","status_code":200,"response_time_ms":50,"user_agent":"wget/1.21","country":"KP"}'
    if ($i % 15 -eq 0) { Write-Host "  req=$i score=$($r.risk_score) level=$($r.risk_level) ai=$($r.ai_score) attack=$($r.attack_type)" }
}

# ─────────────────────────────────────────────
# 4. ENUMERATION — triggers: consecutive_404s, sequential_endpoint_patterns
# ─────────────────────────────────────────────
Write-Host "`n[4] ENUMERATION — 10.0.0.13" -ForegroundColor Magenta
for ($i = 1; $i -le 25; $i++) {
    $body = "{`"ip`":`"10.0.0.13`",`"method`":`"GET`",`"endpoint`":`"/api/users/$i`",`"status_code`":404,`"response_time_ms`":20,`"user_agent`":`"python-requests/2.28`",`"country`":`"IR`"}"
    $r = Send $body
    if ($i % 5 -eq 0) { Write-Host "  req=$i score=$($r.risk_score) level=$($r.risk_level) ai=$($r.ai_score) attack=$($r.attack_type)" }
}

# ─────────────────────────────────────────────
# 5. SQL INJECTION — triggers: injection_payload rule + ML error_rate
# ─────────────────────────────────────────────
Write-Host "`n[5] SQL INJECTION — 10.0.0.14" -ForegroundColor DarkRed
$injections = @(
    '{"ip":"10.0.0.14","method":"GET","endpoint":"/search?q=UNION SELECT password FROM users","status_code":500,"response_time_ms":200,"user_agent":"sqlmap/1.7","country":"CN"}',
    '{"ip":"10.0.0.14","method":"GET","endpoint":"/user?id=1 OR 1=1--","status_code":200,"response_time_ms":150,"user_agent":"sqlmap/1.7","country":"CN"}',
    '{"ip":"10.0.0.14","method":"GET","endpoint":"/etc/passwd","status_code":404,"response_time_ms":10,"user_agent":"nikto/2.1","country":"CN"}',
    '{"ip":"10.0.0.14","method":"POST","endpoint":"/login","status_code":500,"response_time_ms":300,"user_agent":"sqlmap/1.7","country":"CN"}'
)
foreach ($body in $injections) {
    $r = Send $body
    Write-Host "  score=$($r.risk_score) level=$($r.risk_level) ai=$($r.ai_score) attack=$($r.attack_type)"
}

# ─────────────────────────────────────────────
# 6. SENSITIVE ENDPOINTS — triggers: sensitive_endpoint rule
# ─────────────────────────────────────────────
Write-Host "`n[6] SENSITIVE ENDPOINTS — 10.0.0.15" -ForegroundColor DarkYellow
$endpoints = @("/admin","/debug","/.env","/actuator/health","/config","/api-docs","/swagger")
foreach ($ep in $endpoints) {
    $body = "{`"ip`":`"10.0.0.15`",`"method`":`"GET`",`"endpoint`":`"$ep`",`"status_code`":403,`"response_time_ms`":15,`"user_agent`":`"Mozilla/5.0`",`"country`":`"US`"}"
    $r = Send $body
    Write-Host "  $ep -> score=$($r.risk_score) level=$($r.risk_level) ai=$($r.ai_score)"
}

# ─────────────────────────────────────────────
# 7. NORMAL TRAFFIC — for contrast
# ─────────────────────────────────────────────
Write-Host "`n[7] NORMAL TRAFFIC — 10.0.0.20" -ForegroundColor Green
$normal = @(
    '{"ip":"10.0.0.20","method":"GET","endpoint":"/api/products","status_code":200,"response_time_ms":80,"user_agent":"Android-App/4.2","country":"FR"}',
    '{"ip":"10.0.0.20","method":"POST","endpoint":"/login","status_code":200,"response_time_ms":120,"user_agent":"iPhone-iOS16","country":"FR"}',
    '{"ip":"10.0.0.20","method":"GET","endpoint":"/api/profile","status_code":200,"response_time_ms":60,"user_agent":"SamsungBrowser/19","country":"FR"}'
)
foreach ($body in $normal) {
    $r = Send $body
    Write-Host "  score=$($r.risk_score) level=$($r.risk_level) attack=$($r.attack_type)"
}

Write-Host "`n=== Simulation complete ===" -ForegroundColor Green
Write-Host "Open http://localhost:3000 to see results" -ForegroundColor Green
