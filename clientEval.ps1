Install-Module -Name BigFix

$expressions = @('if (exists folder ((value "EnterpriseClientFolder" of keys "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\BigFix\EnterpriseClient" of native registry) as string & "DEX")) then ((not exists (file of folder ((value "EnterpriseClientFolder" of keys "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\BigFix\EnterpriseClient" of native registry) as string & "DEX")) whose ((name of it = "LastArchivalTime.txt"))) or (exists (file of folder ((value "EnterpriseClientFolder" of keys "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\BigFix\EnterpriseClient" of native registry) as string & "DEX")) whose ((name of it = "LastArchivalTime.txt") and (now - modification time of it > 24*hour)))) else false', 'if (exists folder ((value "EnterpriseClientFolder" of keys "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\BigFix\EnterpriseClient" of native registry) as string & "DEX\Results")) then (number of files of folder ((value "EnterpriseClientFolder" of keys "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\BigFix\EnterpriseClient" of native registry) as string & "DEX\Results") > 0) else false', '(name of it, version of it) of operating system')
 
foreach ($expression in $expressions){
 
    $relevance = Invoke-EvaluateClientRelevance $expression
 
    $relevance.Answer
 
}
