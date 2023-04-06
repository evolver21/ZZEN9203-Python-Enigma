# Enigma Encoder - www.101computing.net/enigma-encoder/
### Modified by Enis B - UNSW ZZEN9203

# ----------------- Enigma Settings -----------------
### Starting configuration of the enigma machine
### Chose 3 rotors from I, II, III, IV and V
rotors = ("II", "III", "I")

### Select one of the two rotors UKW-B or UKW-C
reflector = "UKW-B"

### Ring setting relative to the rotor disc. Implemented via the ceasarShift function.
ringSettings = "AAA"

### Starting positions of each ring - left to right
ringPositions = "AAO"

### Plugboard configuration written in pairs, separated by space.
plugboard = "bq cr di ej kw mt os px uz gh"


# ---------------------------------------------------

### Definition of the caesarShift function.
def caesarShift(str, amount):

    output = ""

    ### Iterates through each character and converts to ASCII code
    for i in range(0, len(str)):
        c = str[i]

        ### Return the ASCII value for current letter
        code = ord(c)

        ### Check if ASCII Code is between 65 (A) and 90 (Z) and shift by argument "amount" value.
        ### % 26 is used for simulating a continuous rotor loop
        if ((code >= 65) and (code <= 90)):

            ### Convert back from ASCII code to letters.
            c = chr(((code - 65 + amount) % 26) + 65)

        ### Each processed character is appended to the previous one.
        output = output + c

    return output

### Main encoding function
def encode(plaintext):

    ### Define global variables
    global rotors, reflector, ringSettings, ringPositions, plugboard

    # Enigma Rotors and reflectors
    ### Configuration of letters and notch positions for each rotor
    rotor1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    rotor1Notch = "Q"
    rotor2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    rotor2Notch = "E"
    rotor3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    rotor3Notch = "V"
    rotor4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    rotor4Notch = "J"
    rotor5 = "VZBRGITYUPSDNHLXAWMJQOFECK"
    rotor5Notch = "Z"

    ### Dictionaries with key:value pairs for easier reference
    rotorDict = {"I": rotor1, "II": rotor2, "III": rotor3, "IV": rotor4, "V": rotor5}
    rotorNotchDict = {"I": rotor1Notch, "II": rotor2Notch, "III": rotor3Notch, "IV": rotor4Notch, "V": rotor5Notch}

    ### Defines how each letter is reflected to another for each reflector
    reflectorB = {"A": "Y", "Y": "A", "B": "R", "R": "B", "C": "U", "U": "C", "D": "H", "H": "D", "E": "Q", "Q": "E",
                  "F": "S", "S": "F", "G": "L", "L": "G", "I": "P", "P": "I", "J": "X", "X": "J", "K": "N", "N": "K",
                  "M": "O", "O": "M", "T": "Z", "Z": "T", "V": "W", "W": "V"}
    reflectorC = {"A": "F", "F": "A", "B": "V", "V": "B", "C": "P", "P": "C", "D": "J", "J": "D", "E": "I", "I": "E",
                  "G": "O", "O": "G", "H": "Y", "Y": "H", "K": "R", "R": "K", "L": "Z", "Z": "L", "M": "X", "X": "M",
                  "N": "W", "W": "N", "Q": "T", "T": "Q", "S": "U", "U": "S"}

    ### Letters of the alphabet
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    ### Sets indicators of aligned notch positions to false.
    rotorANotch = False
    rotorBNotch = False
    rotorCNotch = False

    ### Determines which rotor is used. If set to UKW-B it's reflectorB otherwise reflectorC
    if reflector == "UKW-B":
        reflectorDict = reflectorB
    else:
        reflectorDict = reflectorC

    # A = Left,  B = Mid,  C=Right
    ### Sets rotor A, B and C as per user configuration at the script beginning
    rotorA = rotorDict[rotors[0]]
    rotorB = rotorDict[rotors[1]]
    rotorC = rotorDict[rotors[2]]

    ### Sets rotor A, B and C notch positions based on chosen rotors
    ### Rotor A notch is not used in the script, as it's next to the reflector
    rotorANotch = rotorNotchDict[rotors[0]]
    rotorBNotch = rotorNotchDict[rotors[1]]
    rotorCNotch = rotorNotchDict[rotors[2]]

    ### Set starting position for each rotor as per user configuration.
    rotorALetter = ringPositions[0]
    rotorBLetter = ringPositions[1]
    rotorCLetter = ringPositions[2]

    ### Define rotor ring settings relative to the rotor
    rotorASetting = ringSettings[0]
    offsetASetting = alphabet.index(rotorASetting)
    rotorBSetting = ringSettings[1]
    offsetBSetting = alphabet.index(rotorBSetting)
    rotorCSetting = ringSettings[2]
    offsetCSetting = alphabet.index(rotorCSetting)

    ### Set user defined rotor ring settings via the caesarShift function.
    rotorA = caesarShift(rotorA, offsetASetting)
    rotorB = caesarShift(rotorB, offsetBSetting)
    rotorC = caesarShift(rotorC, offsetCSetting)

    #### Reconstruct each rotor based on current offset value using slicing function
    if offsetASetting > 0:
        rotorA = rotorA[26 - offsetASetting:] + rotorA[0:26 - offsetASetting]
    if offsetBSetting > 0:
        rotorB = rotorB[26 - offsetBSetting:] + rotorB[0:26 - offsetBSetting]
    if offsetCSetting > 0:
        rotorC = rotorC[26 - offsetCSetting:] + rotorC[0:26 - offsetCSetting]

    ### Define variable "ciphertext" and set to blank.
    ciphertext = ""

    # Convert plugboard settings into a dictionary
    ### Convert plugboard argument to uppercase, split on space, add key/value pairs into the dictionary
    plugboardConnections = plugboard.upper().split(" ")
    plugboardDict = {}
    for pair in plugboardConnections:
        if len(pair) == 2:
            plugboardDict[pair[0]] = pair[1]
            plugboardDict[pair[1]] = pair[0]

    ### Convert the input to uppercase. Keyboard input is defined as plaintext in the script regardless if encrypting or decrypting.
    plaintext = plaintext.upper()

    ### Iterate through each letter of the input
    for letter in plaintext:
        encryptedLetter = letter

        ### Logic for rotating rotors if current letter is a valid alphabet letter.
        if letter in alphabet:

            # Rotate Rotors - This happens as soon as a key is pressed, before encrypting the letter!
            ### Reset rotorTrigger
            rotorTrigger = False

            # Third rotor rotates by 1 for every key being pressed
            ### Check if rotor C notch matches the current rotor C letter, set rotorTrigger to true
            if rotorCLetter == rotorCNotch:
                rotorTrigger = True

            ### Iterate rotor C by one letter.
            ### Positional value in alphabet. Mod 26 simulates continuous rotor loop
            rotorCLetter = alphabet[(alphabet.index(rotorCLetter) + 1) % 26]

            # Check if rotorB needs to rotate
            if rotorTrigger:

                ### Reset rotorTrigger
                rotorTrigger = False

                ### Check if rotor B notch matches the current rotor B letter, set rotorTrigger to true
                if rotorBLetter == rotorBNotch:
                    rotorTrigger = True

                ### Iterate rotor B by one letter.
                ### Positional value in alphabet. Mod 26 simulates continuous rotor loop
                rotorBLetter = alphabet[(alphabet.index(rotorBLetter) + 1) % 26]

                # Check if rotorA needs to rotate
                if (rotorTrigger):

                    ### Reset rotorTrigger
                    rotorTrigger = False

                    ### Iterate rotor A by one letter.
                    ### Positional value in alphabet. Mod 26 simulates continuous rotor loop
                    rotorALetter = alphabet[(alphabet.index(rotorALetter) + 1) % 26]

            else:
                # Check for double step sequence!
                ### If rotor B notch matches the current rotor B letter, iterate both rotor B and A by one letter
                if rotorBLetter == rotorBNotch:
                    rotorBLetter = alphabet[(alphabet.index(rotorBLetter) + 1) % 26]
                    rotorALetter = alphabet[(alphabet.index(rotorALetter) + 1) % 26]

            #### Define the encryption step output string
            #### Append the current letter to be encrypted
            output = letter

            # Implement plugboard encryption!
            ### Check if current letter has a matching pair in the plugboard dictionary, and swap it with its value
            if letter in plugboardDict.keys():
                if plugboardDict[letter] != "":
                    encryptedLetter = plugboardDict[letter]
                #### If the letter has a pair in the plugboard, append it to output
                output += " > Plugboard: " + encryptedLetter

            # Rotors & Reflector Encryption
            ### Calculate offset position for each rotor relative to starting letter A
            offsetA = alphabet.index(rotorALetter)
            offsetB = alphabet.index(rotorBLetter)
            offsetC = alphabet.index(rotorCLetter)

            # Wheel 3 Encryption
            ### All wheels have the same logic.
            ### Find positional value of the letter in alphabet
            pos = alphabet.index(encryptedLetter)

            ### Identify the corresponding letter from the rotor definition
            let = rotorC[(pos + offsetC) % 26]

            ### Positional value in alphabet of the new output letter
            pos = alphabet.index(let)

            ### New output/encrypted letter without the offset
            encryptedLetter = alphabet[(pos - offsetC + 26) % 26]

            #### New letter after rotor C encryption, including the offset
            rotorCoutput = alphabet[(pos + 26) % 26]
            #### Append rotor C output to the final output string
            output += " > Rotor C: " + rotorCoutput

            # Wheel 2 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorB[(pos + offsetB) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetB + 26) % 26]

            #### New letter after rotor B encryption, including the offset
            rotorBoutput = alphabet[(pos + 26) % 26]
            #### Append rotor B output to the final output string
            output += " > Rotor B: " + rotorBoutput

            # Wheel 1 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorA[(pos + offsetA) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetA + 26) % 26]

            #### New letter after rotor A encryption, including the offset
            rotorAoutput = alphabet[(pos + 26) % 26]
            #### Append rotor A output to the final output string
            output += " > Rotor A: " + rotorAoutput

            # Reflector encryption!
            ### Returns the corresponding value of the encryptedLetter key from reflector dictionary
            if encryptedLetter in reflectorDict.keys():
                if reflectorDict[encryptedLetter] != "":
                    encryptedLetter = reflectorDict[encryptedLetter]

            #### Append reflector output to the final output string
            output += " > Reflector: " + encryptedLetter

            # Back through the rotors
            # Wheel 1 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetA) % 26]
            pos = rotorA.index(let)
            encryptedLetter = alphabet[(pos - offsetA + 26) % 26]

            #### New letter after rotor A encryption, including the rotor B offset
            rotorAoutput = alphabet[(pos + offsetB - offsetA + 26) % 26]
            #### Append rotor A output to the final output string
            output += " > Rotor A: " + rotorAoutput

            # Wheel 2 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetB) % 26]
            pos = rotorB.index(let)
            encryptedLetter = alphabet[(pos - offsetB + 26) % 26]

            #### New letter after rotor B encryption, including the rotor C offset
            rotorBoutput = alphabet[(pos + offsetC - offsetB + 26) % 26]
            #### Append rotor B output to the final output string
            output += " > Rotor B: " + rotorBoutput

            # Wheel 3 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetC) % 26]
            pos = rotorC.index(let)
            encryptedLetter = alphabet[(pos - offsetC + 26) % 26]

            #### New letter after rotor C encryption, including the offset
            rotorCoutput = alphabet[(pos - offsetC + 26) % 26]
            #### Append rotor C output to the final output string
            output += " > Rotor C: " + rotorCoutput

            # Implement plugboard encryption!
            ### Returns the corresponding value of the encryptedLetter key from plugboard dictionary
            if encryptedLetter in plugboardDict.keys():
                if plugboardDict[encryptedLetter] != "":
                    encryptedLetter = plugboardDict[encryptedLetter]
                #### If the letter has a pair in the plugboard, append it to output
                output += " > Plugboard: " + encryptedLetter


        ### Appends letters to ciphertext as they get encrypted/decrypted one by one
        ciphertext = ciphertext + encryptedLetter
        print(output)
    return ciphertext


# Main Program Starts Here
print("\n##### Enigma Encoder - UNSW ZZEN9203 #####")
print("")
### Prompt for text input
plaintext = input("Enter text to encode or decode: ")

### Call the encode() function passing user plaintext input as argument
ciphertext = encode(plaintext)

### Return the output of encode() function as ciphertext
print("\nEncoded text: \n " + ciphertext)
