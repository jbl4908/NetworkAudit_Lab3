$File = Get-Content -Path E:\addresses.txt

$index = 0
$length = $File.Length

$succ_ip = @()

Do{
    #This loop will have $hostname be the next hostname to get an ip for
    $hostname = $File[$index]
    #Query for the addresses
    $query = [System.Net.Dns]::GetHostAddresses($hostname)
    #Loop below takes the addresses and puts them in the result string
    $result = "$hostname : "
    $index_2 = 0

    #Get each ip and add it to our result string
    Do{
        $addition = $query[$index_2]
        $addition.ToString()
        $result = $result + "$addition, "
        $index_2 += 1
    }While($index_2 -lt ($query.Length))

    #Add the result of this host to our success list
    $succ_ip += $result
    $index += 1
}While($index -lt ($length))

$index = 0
#Here we just print everything in our list of ips
Do{
    Write-Host ""
    Write-Host $succ_ip[$index]
    $index += 1
}While($index -lt ($succ_ip.Length))