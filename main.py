#Function for encryption or decryption 
def caesar(text, shift, encrypt=True):
    
    if not isinstance(shift, int):
        return 'Shift must be an integer value.'
    
    if shift < 1 or shift > 25:
        return 'Shift must be an integer between 1 and 25.'
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    #If its not to encrypt i.e. to decrypt
    if not encrypt:
        shift = -shift
    
    #Concatenation of shifted elements at the end
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    
    #This maps the alphabet to their corresponding alphabet according to shift
    translation_table = str.maketrans(alphabet + alphabet.upper(), shifted_alphabet+shifted_alphabet.upper())
    
    encrypted_text = text.translate(translation_table)
    
    return encrypted_text


def encrypt(text, shift):
    return caesar(text, shift)

def decrypt(text, shift):
    return caesar(text, shift, encrypt=False)

input_text = input("Enter a string: ")
input_shift = int(input("Enter a shift: "))
input_choice = int(input("\n1.Encrypt\n2.Decrypt\nChoice: "))
if input_choice == 1:
    print(encrypt(input_text, input_shift))

elif input_choice == 2:
    print(decrypt(input_text, input_shift))

else:
    print('Invalid choice!!')
    exit 