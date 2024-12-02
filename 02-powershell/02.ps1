function Read-File {
    param ($FilePath)
    Get-Content $FilePath
}

function Is-Safe-Report {
    param ($ReportString)
    $Direction = ""
    $PrevLevel = ""
    $Safe = $true
    $ReportString -Split " " | ForEach-Object {
       $CurrentLevel = [int]$_
       if ($PrevLevel -ne "" ) {
           $distance = ($CurrentLevel - $PrevLevel)
           if ($distance -gt 3 -or $distance -lt -3 -or $distance -eq 0) {
	       $Safe = $false;
	       return
           }
           if ($Direction -eq "") {
		if ($distance -lt 0) { $Direction = "dec" }
       		if ($distance -gt 0) { $Direction = "inc" }
           } else {
		if ($Direction -eq "inc" -and $distance -lt 0) { $Safe = $false; return }
       		if ($Direction -eq "dec" -and $distance -gt 0) { $Safe = $false; return }
           }
       }
       $PrevLevel = $CurrentLevel
    }
    if ($Safe) { return 0 }
    return -1
}

function Solve-Part-One {
    param ($Content)
    $SafeReports = $Content.Length
    foreach ($report in $Content) {
	$SafeReports += (Is-Safe-Report $report)
    }
    Write-Host "Part 1:" $SafeReports
}

function Solve-Part-Two {
    param ($Content)
    $SafeReports = $Content.Length

    :contentLoop foreach ($report in $Content) {
        if ((Is-Safe-Report $report) -eq 0) { continue contentLoop }
	$reportArray = $report.Split(" ")
	for ($i = 0; $i -lt $reportArray.Length; $i++) {
	    $subReport = ""
	    :buildSubReport for ($j = 0; $j -lt $reportArray.Length; $j++) {
	        if ($i -eq $j) { continue buildSubReport }
	        $subReport += " " + $reportArray[$j]
	    }
	    if ((Is-Safe-Report $subReport) -eq 0) { continue contentLoop }
	}
        $SafeReports--
    }
    Write-Host "Part 2:" $SafeReports
}

$InputFile = "../inputs/02.txt"
$Content = (Read-File $InputFile)

Solve-Part-One $Content
Solve-Part-Two $Content
