$iprange = Read-Host -Prompt 'Input IP range'

if($iprange.Contains("-")){
    $succ_ip = New-Object System.Collections.ArrayList
    #First, taking inputs for the ip if - is present
    $iprange_extended = $iprange.Split("{-}")
    $iprange_1 = $iprange_extended[0]
    $iprange_2 = $iprange_extended[1]
    Write-Host "Start IP: $iprange_1"
    Write-Host "End_IP: $iprange_2"

    #Set up both the numeral and string representations
    $iprange_1_split = $iprange_1.Split("{.}")
    $iprange_2_split = $iprange_2.Split("{.}")
    $int1 = [int]$iprange_1_split[0]
    $int2 = [int]$iprange_1_split[1]
    $int3 = [int]$iprange_1_split[2]
    $int4 = [int]$iprange_1_split[3]
    $ip_current_number = ($int1 * 1000000000) + ($int2 * 1000000) + ($int3 * 1000) + ($int4)
    #Write-Host $ip_current_number
    $int1 = [int]$iprange_2_split[0]
    $int2 = [int]$iprange_2_split[1]
    $int3 = [int]$iprange_2_split[2]
    $int4 = [int]$iprange_2_split[3]
    $ip_end_number = ($int1 * 1000000000) + ($int2 * 1000000) + ($int3 * 1000) + ($int4)
    #add 1 to include the last ip added
    $ip_end_number += 1
    #Write-Host $ip_end_number
    #So now, while ip_current is less than ip_end we will ping and record the ip assosciated with current
    #held in $iprange_1_split concatenated. if Status :Success was in the result we will add it to our list of
    #succesful ip addresses. Use $succ_ip.Add(iprange_1_split[0] + iprange_1_split[1] + iprange_1_split[2] + iprange_1_split[3]
    #After, we will increment both ip_current and iprange_1_split by 1

    Do {
        #Zero stands for success, 1 stands for failure
        $success = 1
        $ip1 = $iprange_1_split[0]
        $ip2 = $iprange_1_split[1]
        $ip3 = $iprange_1_split[2]
        $ip4 = $iprange_1_split[3]
        $query = "$ip1.$ip2.$ip3.$ip4"
        Write-Host "Query: $query"
        if (Test-Connection $query -Quiet){
            #Write-Host "Result test: $result"
            $success = 0
        } else {
            $success = 1
        }
        #$result = Start-Process 'C:\Windows\system32\PING.EXE $query'
        #Write-Host "Result ping: $result"
        #TODO here we will put the if
        if ($success -lt 1){
            $succ_ip.Add($query) > $null
        }
        #Now to increment ip current number
        #and now increment our actual string
        $ip_add = [int]$iprange_1_split[3]
        $ip_add += 1
        if ($ip_add -gt 254) {
            #if the farthest octet gets to 255, increase the next left octet by one and set farthest to 1
            $ip_add_2 = [int]$iprange_1_split[2]
            $ip_add_2 += 1
            $ip_add_2.ToString()
            $iprange_1_split[2] = $ip_add_2
            $ip_add = 1
            $ip_current_number = $ip_current_number - 253
            $ip_current_number += 1000
        } else {
            $ip_current_number += 1
        }
        $ip_add.ToString()
        $iprange_1_split[3] = $ip_add
        Write-Host $ip_current_number

    } While ($ip_current_number -lt $ip_end_number)
    Write-Host "IP that are up: $succ_ip"

}
else{
    $succ_ip = New-Object System.Collections.ArrayList
    $iprange_no = $iprange.Split("{/}")
    $sub = $iprange[1]
    $iprange_no = $iprange_no[0]
    $iprange_values = $iprange_no.Split("{.}")
    $ip4 = [int]$iprange_values[3]
    $ip3 = [int]$iprange_values[2]
    if ($iprange.Contains("16")){
        #Here we do the farthest two octets
        Write-Host "Got 16"
        $iprange_1_split = $iprange_no.Split("{.}")
        $int1 = [int]$iprange_1_split[0]
        $int2 = [int]$iprange_1_split[1]
        $int3 = [int]$iprange_1_split[2]
        $int4 = [int]$iprange_1_split[3]
        $ip_current_number = ($int1 * 1000000000) + ($int2 * 1000000) + ($int3 * 1000) + ($int4)
        $ip_end_number = ($int1 * 1000000000) + ($int2 * 1000000) + (254 * 1000) + (254)

        Do {
            #Zero stands for success, 1 stands for failure
            $success = 1
            $ip1 = $iprange_1_split[0]
            $ip2 = $iprange_1_split[1]
            $ip3 = $iprange_1_split[2]
            $ip4 = $iprange_1_split[3]
            $query = "$ip1.$ip2.$ip3.$ip4"
            Write-Host "Query: $query"
            if (Test-Connection $query -Quiet){
                #Write-Host "Result test: $result"
                $success = 0
            } else {
                $success = 1
            }
            #$result = Start-Process 'C:\Windows\system32\PING.EXE $query'
            #Write-Host "Result ping: $result"
            #TODO here we will put the if
            if ($success -lt 1){
                $succ_ip.Add($query) > $null
            }
            #Now to increment ip current number
            #and now increment our actual string
            $ip_add = [int]$iprange_1_split[3]
            $ip_add += 1
            if ($ip_add -gt 254) {
                #if the farthest octet gets to 255, increase the next left octet by one and set farthest to 1
                $ip_add_2 = [int]$iprange_1_split[2]
                $ip_add_2 += 1
                $ip_add_2.ToString()
                $iprange_1_split[2] = $ip_add_2
                $ip_add = 1
                $ip_current_number = $ip_current_number - 253
                $ip_current_number += 1000
            } else {
                $ip_current_number += 1
            }
            $ip_add.ToString()
            $iprange_1_split[3] = $ip_add
            #Write-Host $ip_current_number

        } While ($ip_current_number -lt $ip_end_number)
        Write-Host "IP that are up: $succ_ip"
    }
    if ($iprange.Contains("24")){
        #Here we do the farthest octet
        Write-Host "Got 24"
        $iprange_1_split = $iprange_no.Split("{.}")
        $int1 = [int]$iprange_1_split[0]
        $int2 = [int]$iprange_1_split[1]
        $int3 = [int]$iprange_1_split[2]
        $int4 = [int]$iprange_1_split[3]
        $ip_current_number = ($int1 * 1000000000) + ($int2 * 1000000) + ($int3 * 1000) + ($int4)
        $ip_end_number = ($int1 * 1000000000) + ($int2 * 1000000) + ($int3 * 1000) + (254)

        Do {
            #Zero stands for success, 1 stands for failure
            $success = 1
            $ip1 = $iprange_1_split[0]
            $ip2 = $iprange_1_split[1]
            $ip3 = $iprange_1_split[2]
            $ip4 = $iprange_1_split[3]
            $query = "$ip1.$ip2.$ip3.$ip4"
            Write-Host "Query: $query"
            if (Test-Connection $query -Quiet){
                #Write-Host "Result test: $result"
                $success = 0
            } else {
                $success = 1
            }
            #$result = Start-Process 'C:\Windows\system32\PING.EXE $query'
            #Write-Host "Result ping: $result"
            #TODO here we will put the if
            if ($success -lt 1){
                $succ_ip.Add($query) > $null
            }
            #Now to increment ip current number
            #and now increment our actual string
            $ip_add = [int]$iprange_1_split[3]
            $ip_add += 1
            if ($ip_add -gt 254) {
                #if the farthest octet gets to 255, increase the next left octet by one and set farthest to 1
                $ip_add_2 = [int]$iprange_1_split[2]
                $ip_add_2 += 1
                $ip_add_2.ToString()
                $iprange_1_split[2] = $ip_add_2
                $ip_add = 1
                $ip_current_number = $ip_current_number - 253
                $ip_current_number += 1000
            } else {
                $ip_current_number += 1
            }
            $ip_add.ToString()
            $iprange_1_split[3] = $ip_add
            #Write-Host $ip_current_number

        } While ($ip_current_number -lt $ip_end_number)
        Write-Host "IP that are up: $succ_ip"
    }
    elseif ($ip4 -gt 0){
        #In this case, we can just ping the ip in $iprange and return the result since we were given a single i
        if (Test-Connection $iprange_no -Quiet){
            #Write-Host "Result test: $result"
            $succ_ip.Add($iprange_no) > $null
        } else {
            $success = 1
        }
        Write-Host "IP that are up: $succ_ip"
    } else {
        #In this case, we are gonna have to go through everything 1-254 for either field with 0
        Write-Host "Case not accounted for"
    }
    #Write-Host "Scanning $iprange :"
    #Write-Host $iprange_values[3]
}