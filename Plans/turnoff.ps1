#
#	This script does simple things but oh so well :)
#	@Author: Mr.Rebel
#
# Get Box Name run as ./turnoff.ps1 box_name (LOWERCASE!!!!)
#Set-ExecutionPolicy RemoteSigned
#./MpCmdRun.exe -Scan -ScanType 2
#https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-antivirus/command-line-arguments-windows-defender-antivirus

param(
      [Parameter(Mandatory = $True,valueFromPipeline=$true)][String] $box
)

echo "*************************************"
echo "RUNNING FOR BOX: $box"
echo "*************************************"

function build_wall{
	echo "Putting old rules into rules.txt!!!!"
	Get-NetFirewallRule | Out-File -FilePath .\rules.txt -NoClobber
	echo "Restoring firewall rules to default"
	netsh advfirewall reset
	netsh advfirewall set allprofiles state on
	netsh advfirewall firewall delete rule name=all
	netsh advfirewall set allprofiles firewallpolicy blockinbound,blockoutbound
	#Remove-NetFirewallRule -All
	echo "*****************************"
	echo "BUILDING WALL"
	echo "*****************************"
	for($num = 21; $num -lt 2000; $num++){
	#depending on box we don't want to block certain ports
	if($num -eq 80 -OR $num -eq 443 -OR $num -eq 53 -OR $num -eq 514){
		continue
	}
	if(($num -eq 22 -OR $num -eq 23) -AND $box -eq "Bonaparte"){
		continue
	}
	if(($num -eq 67 -OR $num -eq 68) -AND $box -eq "Sulleyman"){
		continue
	}
	if(($num -eq 25 -OR $num -eq 143 -OR $num -eq 993 -OR $num -eq 465 -OR $num -eq 110) -AND $box -eq "Xerxes" ){
		continue
	}
	if(($num -eq 636 -OR $num -eq 389 -OR $num -eq 88 -OR $num -eq 445) -AND $box -eq "Alexander"){
		continue
	}
	if(($num -eq 21 -OR $num -eq 445 -OR $num -eq 139 -OR $num -eq 123 -OR $num -eq 42) -AND $box -eq "Julius"){
		continue
	}
	echo "Blocking port + $num"
	echo "Blocking TCP"
	netsh advfirewall firewall add rule name="Blocktcp_in + $num" protocol=TCP dir=in localport=$num action=block
	netsh advfirewall firewall add rule name="Blocktcp_out + $num" protocol=TCP dir=out localport=$num action=block
	echo "Blocking UDP"
	netsh advfirewall firewall add rule name="Blocktcp_in + $num" protocol=UDP dir=in localport=$num action=block
	netsh advfirewall firewall add rule name="Blocktcp_out + $num" protocol=UDP dir=out localport=$num action=block
	}

	# Sleep for 180 seconds before running again
	#Start-Sleep -s 180
}

function stop_process{
	$tasklist = tasklist.exe
	$tasklist = $tasklist.Split(" ")
	$truetaskList =  @()

	ForEach($task in $tasklist){
		if (($task -match '.exe' -OR -$task -match '.py' -OR $task -match '.ps1') -and -Not($truetaskList.Contains($task)) -and -Not($task -match 'powershell')){
			$truetaskList += $task
		}
	}

	ForEach($task in $truetaskList){
		Try{
			$truetask = $task.Substring(0,$task.Length-4)
            if($truetask -eq "powershell.exe" -OR $truetask -eq "turnoff.ps1"){
                continue
            }
			echo "Stopping: $truetask"
			Stop-Process -Name $truetask
		}
		Catch{
			continue
		}
	}
}

function change_users{
	$Accounts =  Get-WmiObject -Class Win32_UserAccount -filter "LocalAccount = True"
	$ListUsers = @()
	$currentuser = $env:USERNAME
	$Accounts = $Accounts -split ' '
	ForEach($account in $Accounts){
		$stringAccount = [string]$account -split '"'
		for($i = 0; $i -lt $stringAccount.Count; $i+=1){
			if ($i -eq 3){
				$user = $stringAccount[$i]
				$ListUsers += $user
			}
		 }
	}
	#Disable-LocalUser -Name $username
	$Password = (ConvertTo-SecureString -AsPlainText "TenToesDownForLife$10!" -Force)
	ForEach($user in $ListUsers){
		Try{
			echo "Changing password for User: $user"
			$User | Set-LocalUser -Password $Password
			echo "Successfully changed password for $User"
		}
		Catch{
			$string_err = $_ | Out-String
			echo $string_err
			continue
		}
	}
}

function scan{
	echo "Starting quick scan!!!!!!!"
	Try{
		Set-MpPreference -ScanParameters 2 -ScanScheduleDay 0 -ScanScheduleQuickScanTime 1 -UnknownThreatDefaultAction "Quarantine" -SevereThreatDefaultAction "Quarantine" -HighThreatDefaultAction "Quarantine" -LowThreatDefaultAction "Quarantine" -ModerateThreatDefaultAction "Quarantine" -CheckForSignaturesBeforeRunningScan 1 -DisableRealtimeMonitoring 0
		Start-MpScan -ThrottleLimit 0 -ScanType 1
		echo "Sleeping for 30 seconds then running full scan!"
		Start-Sleep 30
		Start-MpScan -ThrottleLimit 0 -ScanType 2
	}
	Catch{
		Try{
			C:\"Program Files"\"Windows Defender"\MpCmdRun.exe -Scan -ScanType 1
			echo "Sleeping for 60 seconds then running full scan!"
			Start-Sleep 30
			C:\"Program Files"\"Windows Defender"\MpCmdRun.exe -Scan -ScanType 2
		 }
		 Catch{
			$string_err = $_ | Out-String
            echo $string_err
		 }
	}
}

function main{
	Clear
    #$UserAccount = Get-LocalUser -Name "Administrator"
	if (-not($box -eq "Julius")){
		# Disable SMB if not scored service!
        Try{
		echo "Disabling SMB1"
		Disable-WindowsOptionalFeature -Online -FeatureName 'SMB1Protocol' -ErrorAction SilentlyContinue -WarningAction SilentlyContinue -NoRestart | Out-Null
 		echo "Disabling SMB2"
		if(-not($box -eq "Alexander")){
			Set-SmbServerConfiguration -EnableSMB2Protocol $false
			echo "Disabling SMB3"
			Set-SmbServerConfiguration -EnableSMB3Protocol $false
        }
	    Catch{
		        $string_err = $_ | Out-String
		        echo $string_err
	    }
	}
	echo "Disabling RDP!!!"
	if((-not($box -eq "Alexander") -AND (-not($box -eq "Bonaparte")))){
		try{
			Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
			echo "RDP Disabled"
		}
		Catch{
			$string_err = $_ | Out-String
			echo $string_err
		}
	}
	# set mp preferences
    # set environment policy and rerun script!!!
	echo "Setting lockdown policy"
	Try{
		[Environment]::SetEnvironmentVariable('__PSLockdownPolicy', '4', 'Machine')
	}
	Catch{
		 $string_err = $_ | Out-String
		 echo $string_err
	}
	change_users
	#stop_process
	build_wall
	scan
}

main