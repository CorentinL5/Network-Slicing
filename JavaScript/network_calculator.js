function ipToInt(ip){
    return ip.split('.').reduce((int, octet) => (int << 8) + parseInt(octet, 10), 0) >>> 0;
}

function intToIp(int) {
    return `${(int >>> 24)}.${(int >> 16 & 255)}.${(int >> 8 & 255)}.${(int & 255)}`;
}

function maskToBinary(mask) {
    return '1'.repeat(mask) + '0'.repeat(32 - mask);
}

function maskToIp(mask) {
    return intToIp(parseInt(maskToBinary(mask), 2));
}


function calculateNetworkInfo(previousBroadcast, groupSize){
    const newMask = 32 - Math.ceil(Math.log2(groupSize + 2));
    const addressAvailable = Math.pow(2, 32 - newMask);
    const networkAddressInt = previousBroadcast + 1;
    const broadcastAddressInt = networkAddressInt + addressAvailable - 1;
    const networkAddress = intToIp(networkAddressInt);
    const broadcastAddress = intToIp(broadcastAddressInt);
    const addressRange = `${networkAddress} - ${broadcastAddress}`;

    return [networkAddress, broadcastAddress, addressRange, addressAvailable, newMask];
}

function isNetworkAddress(ip, mask) {
    const ipInt = ipToInt(ip);
    const maskInt = ~((1 << (32 - mask)) - 1);
    return (ipInt % maskInt) === 0;
}

function validateInputs() {
    try {
        const baseNetworkIP = document.getElementById('entryBaseNetworkIP').value;
        const baseNetworkMask = parseInt(document.getElementById('entryBaseNetworkMask').value);
        const listOfGroups = document.getElementById('entryListOfGroups').value.split(',').map(x => parseInt(x));


        if (!/^(\d{1,3}\.){3}\d{1,3}$/.test(baseNetworkIP)) {
            new Error('Invalid IP address format.');
        }
        if (!(0 <= baseNetworkMask && baseNetworkMask <= 32)) {
            new Error('The subnet mask must be between 0 and 32 inclusive.');
        }
        if (!listOfGroups.every(groupSize => Number.isInteger(groupSize) && groupSize > 0)) {
            new Error('Group sizes must be positive integers.');
        }

        return true;
    } catch (e) {
        alert(`Input error: ${e.message}`);
        return false;
    }
}

function displayResults()  {
    if (!validateInputs()) {
        return;
    }

    const baseNetworkIP = document.getElementById('entryBaseNetworkIP').value;
    const baseNetworkMask = parseInt(document.getElementById('entryBaseNetworkMask').value);
    const listOfGroups = document.getElementById('entryListOfGroups').value.split(',').map(x => parseInt(x)).sort((a, b) => b - a);

    // Options for the base network IP
    const showMaskIp = document.getElementById('showMaskIp').checked;
    const showMaskBinary = document.getElementById('showMaskBinary').checked;

    let previousBroadcast;
    if (isNetworkAddress(baseNetworkIP, baseNetworkMask)) {
        previousBroadcast = ipToInt(baseNetworkIP) - 1;
    } else {
        previousBroadcast = ipToInt(baseNetworkIP) + Math.pow(2, 32 - baseNetworkMask) - 1;
    }

    const resultText = document.getElementById('resultText');
    resultText.value = ''; // Clear previous results

    for (const groupSize of listOfGroups) {
        const [networkAddress, broadcastAddress, addressRange, addressAvailable, subnetMask] = calculateNetworkInfo(previousBroadcast, groupSize);
        previousBroadcast = ipToInt(broadcastAddress);

        resultText.value += `For group size ${groupSize}:\n`;
        resultText.value += `Network Address: ${networkAddress}\n`;
        resultText.value += `Broadcast Address: ${broadcastAddress}\n`;
        resultText.value += `Address Range: ${addressRange}\n`;
        resultText.value += `Subnet Mask, : /${subnetMask}\n`;
        if (showMaskIp) {
            resultText.value += `Subnet Mask, IP: ${maskToIp(subnetMask)}\n`;
        }
        if (showMaskBinary) {
            resultText.value += `Subnet Mask, Binary: ${maskToBinary(subnetMask)}\n`;
        }
        resultText.value += `Number of Addresses, Theoretical: ${addressAvailable}, Available: ${addressAvailable - 2}\n\n`;
    }
    resultText.rows = resultText.value.split('\n').length;
    //show the result:
    resultText.style.display = 'block';
}
