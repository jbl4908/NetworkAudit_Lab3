function IP-toINT64 ($ip) {  
 
  $octets = $ip.split(".") 
  return [int64]([int64]$octets[0]*16777216 +[int64]$octets[1]*65536 +[int64]$octets[2]*256 +[int64]$octets[3]) 
}
 
function INT64-toIP([int64]$int) { 

  return (([math]::truncate($int/16777216)).tostring()+"."+([math]::truncate(($int%16777216)/65536)).tostring()+"."+([math]::truncate(($int%65536)/256)).tostring()+"."+([math]::truncate($int%256)).tostring() )
}

function scan_addr($ip,$port){
    try{
        $socket = New-Object System.Net.Sockets.TcpClient($ip,$port)
    } catch {
        return $_.Exception.innerexception.ErrorCode
    }
    return 0
}


function parse_port($port_string){
    $port_string = $port_string.Split("-")
    $ports = New-Object System.Collections.ArrayList
    if ($port_string.Length -eq 1){
        $port_string = $port_string[0].Split(",")
        if ($port_string.Length -eq 1){
            $ports.Add([int]$port_string[0])
        } else {
            foreach($i in $port_string){
                $ports.Add(([int]$i))
            }
        }
    } else {
        for($i = ([int]$port_string[0]); $i -le [int]$port_string[1]; $i++){
            $ports.Add($i)
        }
    }
    return $ports
}


function scan-ports($ip,$ports){
    foreach($port in $ports){
        $status = scan_addr -ip $ip -port $port
        switch ($status){
            0 { $result = "Open" }
            10061 {$result = "Closed"}
            10060 {$result = "Blocked by firewall or the computer is down"}
            default {$result = "Closed"}
        }
        if ($status -eq 0) {Write-Host("IP: $ip Port: $port is Open")}
    }
}



$ip = Read-Host -Prompt "Please input IP address (1.1.1.1) or IP range(1.1.1.1-2.2.2.3)"
$start_end = $ip.Split("-")

$port_string = Read-Host -Prompt "Please input port(s)"
$ports= parse_port -port_string $port_string
$midindex = [int]($ports.Length/2)
$ports = $ports[$midindex..($ports.Length-1)]

if ($start_end.Length -eq 1){
    $ip = $start_end[0]
    scan-ports -ip $ip -ports $ports
} else {
    $startaddr = IP-toINT64($start_end[0])
    $endaddr = IP-toINT64($start_end[1])
    for ($i = $startaddr; $i -le $endaddr; $i++){
        if (($i%256 -eq 0) -or ($i%256 -eq 255)) {continue}
        $ip = INT64-toIP($i)
        scan-ports -ip $ip -ports $ports
    }
}
