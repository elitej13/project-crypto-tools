import sympy as sy
import kivy
import Crack_RSA as RSA
from time import perf_counter
from random import randint
kivy.require('1.10.0')

if not True:
    import codecs

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock




class Main(BoxLayout):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.menu = Menu(self, orientation='vertical')
        self.add_widget(self.menu)

    def switchToRSAScreen(self, priorScreen):
        self.remove_widget(priorScreen)
        self.rsa = RSAScreen(self, orientation='vertical')
        self.add_widget(self.rsa)

    def switchToHillScreen(self, priorScreen):
        self.remove_widget(priorScreen)
        self.hill = HillScreen(self, orientation='vertical')
        self.add_widget(self.hill)


class Menu(BoxLayout):
    def __init__(self, main, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.main = main

        self.title = Label(text='Choose an Encryption Scheme')
        self.rsa = Button(text='RSA')
        self.hill = Button(text='Hill Cipher')

        self.add_widget(self.title)
        self.add_widget(self.rsa)
        self.add_widget(self.hill)

        def rsa_click(instance):
            self.main.switchToRSAScreen(self)
        def hill_click(instance):
            self.main.switchToHillScreen(self)

        self.rsa.bind(on_press=rsa_click)
        self.hill.bind(on_press=hill_click)




class RSAScreen(BoxLayout):
    def __init__(self, main, **kwargs):
        super(RSAScreen, self).__init__(**kwargs)

        self.first_screen = BoxLayout(orientation='vertical')
        self.second_screen = BoxLayout(orientation='vertical')
#------------------------First Screen----------------------------#
        self.title = Label(text="RSA Encryption")

        self.p = BoxLayout(orientation='horizontal')
        self.p_label = Label(text='Choose a number')
        self.p_input = TextInput(multiline=False)
        self.p.add_widget(self.p_label)
        self.p.add_widget(self.p_input)
        self.p_result = Label()

        self.q = BoxLayout(orientation='horizontal')
        self.q_label = Label(text='Choose a number')
        self.q_input = TextInput(multiline=False)
        self.q.add_widget(self.q_label)
        self.q.add_widget(self.q_input)
        self.q_result = Label()

        self.confirm = Button(text="Confirm Choices")

        self.p_was_chosen = False
        self.q_was_chosen = False

        self.first_screen.add_widget(self.title)
        self.first_screen.add_widget(self.p)
        self.first_screen.add_widget(self.p_result)
        self.first_screen.add_widget(self.q)
        self.first_screen.add_widget(self.q_result)
        self.first_screen.add_widget(self.confirm)

        self.add_widget(self.first_screen)

        def p_validate(instance):
            p = int(self.p_input.text)
            self.p_choice = sy.nextprime(p)
            if(self.p_choice == 2):
                self.p_choice = sy.nextprime(self.p_choice)
            self.p_result.text = "The next prime found was " + str(self.p_choice)
            self.p_was_chosen = True
        def q_validate(instance):
            q = int(self.q_input.text)
            self.q_choice = sy.nextprime(q)
            if(self.q_choice == 2):
                self.q_choice = sy.nextprime(self.q_choice)
            self.q_result.text = "The next prime found was " + str(self.q_choice)
            self.q_was_chosen = True
        def confirm(instance):
            if(self.p_was_chosen & self.q_was_chosen):
                init_second_screen()

        self.p_input.bind(on_text_validate=p_validate)
        self.q_input.bind(on_text_validate=q_validate)
        self.confirm.bind(on_press=confirm)

#------------------------Second Screen----------------------------#
        self.key_pub = Label()
        self.key_pri = Label()
        self.crack = BoxLayout(orientation='horizontal')
        self.rsa_crack = Button(text="Attempt to Crack using Brute Force")
        self.crack_result = Label()
        self.crack.add_widget(self.rsa_crack)
        self.crack.add_widget(self.crack_result)
        self.crack_info = BoxLayout(orientation='horizontal')
        self.thread_count = TextInput(text="How many Threads?")
        self.max_time = TextInput(text="Give up after how many seconds? (Use Zero for no time limit)")
        self.crack_info.add_widget(self.thread_count)
        self.crack_info.add_widget(self.max_time)

        self.second_screen.add_widget(self.key_pub)
        self.second_screen.add_widget(self.key_pri)
        self.second_screen.add_widget(self.crack_info)
        self.second_screen.add_widget(self.crack)

        def is_number(n):
            try:
                int(n)
                return True
            except ValueError:
                return False

        def crack_rsa(instance):
            if(is_number(self.thread_count.text) and is_number(self.max_time.text)):
                thread_count = int(self.thread_count.text)
                max_time = int(self.max_time.text)
                if(thread_count > 64):
                     thread_count = 64
                if(thread_count < 1):
                    thread_count = 1
                if(max_time < 0):
                    max_time = 0
            self.threads = []
            def check_on_crack(dt):
                is_done = False
                is_timed_out = False
                for i in range(len(self.threads)):
                    if(not self.threads[i].isAlive()):
                        self.rsa_crack_stop_time = perf_counter()
                        if(self.threads[i].found == -1):
                            is_timed_out = True
                            break
                        else:
                            is_done = True
                            break
                if(is_done):
                    self.crack_result.text = "Cracked it in " + str(format(self.rsa_crack_stop_time - self.rsa_crack_start_time, '.4f')) + " seconds."
                elif(is_timed_out):
                    self.crack_result.text = "Failed to crack - timed out."
                else:
                    Clock.schedule_once(check_on_crack, 0)
            if(max_time == 0):
                for i in range(thread_count):
                    self.threads.append(RSA.RSA_Cracking_Thread(i + 1, thread_count, "RSA-" + str(i + 1), self.n))
            else:
                for i in range(thread_count):
                    self.threads.append(RSA.RSA_Cracking_Thread_Timed(i + 1, thread_count, "RSA-" + str(i + 1), self.n, max_time))
            self.rsa_crack_start_time = perf_counter()
            self.rsa_crack_stop_time = 0
            for i in range(thread_count):
                self.threads[i].start()
            self.crack_result.text = "Calculating..."
            Clock.schedule_once(check_on_crack, -1)

        def init_second_screen():
            self.remove_widget(self.first_screen)
            p = self.p_choice
            q = self.q_choice
            self.n = p * q
            phi = (p - 1) * (q - 1)
            e = sy.prevprime(int(phi / 2))
            while(sy.gcd(e,phi) != 1):
                e = sy.nextprime(e)
                if(e > phi):
                    e = sy.nextprime(e % phi)
            d = sy.invert(e, phi)
            self.key_pub.text = "Public key (e, n) = (" + str(e) + "," + str(self.n) + ")"
            self.key_pri.text = "Private key (d, n) = (" + str(d) + "," + str(self.n) + ")"
            if(len(self.key_pub.text) > 100):
                self.key_pub.text = "Public key (e, n) = \n(" + str(e) + ",\n" + str(self.n) + ")"
            if(len(self.key_pri.text) > 100):
                self.key_pri.text = "Private key (d, n) = \n(" + str(d) + ",\n" + str(self.n) + ")"

            self.rsa_crack.bind(on_press=crack_rsa)
            self.add_widget(self.second_screen)





class HillScreen(BoxLayout):
    def __init__(self, main, **kwargs):
        super(HillScreen, self).__init__(**kwargs)

#--------------------------Selection Screen-----------------------//
        self.selection_screen = BoxLayout(orientation='vertical')
        self.selection_encryption = Button(text='Encrypt')
        self.selection_decryption = Button(text='Decrypt')

        self.selection_screen.add_widget(self.selection_encryption)
        self.selection_screen.add_widget(self.selection_decryption)

#--------------------------Decryption Screen-----------------------//

        self.add_widget(self.selection_screen)

        def is_number(n):
            try:
                int(n)
                return True
            except ValueError:
                return False

#nxn matrix with random entries mod m with det != 0 or 1...returns the matrix
        def generate_random_matrix(n, m):
            matrix = sy.zeros(n, n)
            while(matrix.det() % m == 0 or matrix.det() % m == 1):
                for i in range(n):
                    for j in range(n):
                        matrix[i, j] = randint(0, m)
            return matrix
        def alpha_to_num(a):
            n = ord(a)
            if(n == 120):
                n = 39
            if(n == 121):
                n = 96
            n -= 32
            if(n >= 89 or n < 0):
                n = 0
            return n
        def num_to_alpha(n):
            n += 32
            if(n == 96):
                n = 121
            if(n == 39):
                n = 120
            return chr(n)
 #Key matrix (for encryption or decryption), message to be ciphered, nxn size of key, mod m... returns a string
        def hill_cipher(key, message, n, m):
            z = int(len(message) / n)
            blocks = [] #message broken up into nx1 vectors and converted to ascii
            for i in range(z):
                block = []
                for j in range(n):
                    block.append(alpha_to_num(message[j + i * n]))
                blocks.append(sy.Matrix(block))
            cipher = [] #next each block is multiplied by the key
            for i in range(z):
                cipher.append(key * blocks[i])
            ciphered = "" #finally each cipher block is taken mod 127 and converted back from a string
            for i in range(z):
                for j in range(n):
                    ciphered += num_to_alpha(int(cipher[i][j]) % m)
            return ciphered

        def encrypt(instance):
            n = self.blocksize.text
            if(is_number(n)):
                n = int(n)
                m = 89 #alphabet size (all ascii characters excluding)
                key = generate_random_matrix(n, m)
                self.encrypted_message = hill_cipher(key, self.message.text, n, m)
                self.result_cipher.text = "Encrypted Message: " + self.encrypted_message + "\n" + "Key: " + str(key)
                print(self.encrypted_message)
                decrypted_message = hill_cipher(key.inv_mod(m), self.encrypted_message, n, m)
                print(decrypted_message)

        def encrypt_message_validate(instance):
            m = self.message.text
            l = len(m)
            while(sy.isprime(l)):
                self.message.text += " "
                m = self.message.text
                l = len(m)
            b = sy.divisors(l)
            self.dropdown = DropDown();
            for i in range(len(b) - 2):
                btn = Button(text=str(b[i + 1]), size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                self.dropdown.add_widget(btn)
            self.blocksize.bind(on_release=self.dropdown.open)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self.blocksize, 'text', x))

        def init_encryption_screen(instance):
            self.encryption_screen = BoxLayout(orientation='vertical')
            self.instruction = Label(text="Enter a message to be encrypted then press enter to generate posible block sizes.")
            self.message = TextInput(multiline=False)
            self.cont = BoxLayout(orientation='horizontal')
            self.blocksize = Button(text="Block Size")
            self.generate = Button(text="Encrypt")
            self.cont.add_widget(self.blocksize)
            self.cont.add_widget(self.generate)
            self.result_cipher = Label()

            self.encryption_screen.add_widget(self.instruction)
            self.encryption_screen.add_widget(self.message)
            self.encryption_screen.add_widget(self.cont)
            self.encryption_screen.add_widget(self.result_cipher)

            self.remove_widget(self.selection_screen)
            self.add_widget(self.encryption_screen)

            self.message.bind(on_text_validate=encrypt_message_validate)
            self.generate.bind(on_press=encrypt)

        def decrypt(instance):
            if(self.validated == False):
                decrypt_message_validate()
                if(self.validated == False):
                    return
            decrypted_message = hill_cipher(self.key.inv_mod(89), self.message.text, self.n, 89)
            print(decrypted_message)
            self.result.text = "Decrypted Message: " + decrypted_message + "\n Inverse Mod Key: " + str(self.key.inv_mod(89))

        def decrypt_message_validate(instance):
            vects = self.key_field.text.split("],[")
            n = len(vects)
            matrix = sy.zeros(n,n)
            alpha_matrix = []
            for i in range(n):
                vects[i] = vects[i].replace("[", "")
                vects[i] = vects[i].replace("]","")
                nums = vects[i].split(",")
                if(len(nums) != n):
                    self.result.text = "Error: Unable to parse key!\nIs it formatted right? Is it an nxn matrix?"
                    return
                alpha_matrix.append(nums)
            print(alpha_matrix)
            for i in range(n):
                for j in range(n):
                    if(is_number(alpha_matrix[i][j]) == False):
                        self.result.text = "Error: Unable to parse key!\nWere all the entries actually numbers?"
                        return
                    matrix[i,j] = int(alpha_matrix[i][j])
            if(matrix.det() == 0 or matrix.det() == 1):
                self.result.text = "Error: Invalid key.\nRemeber the determinant cannot be 0 or 1 for our alphabet."
            self.key = matrix;
            while(len(self.message.text) % n != 0):
                print("Padding with a space.")
                self.message.text += " "
            self.n = n
            self.validated = True

        def init_decryption_screen(instance):
            self.decryption_screen = BoxLayout(orientation='vertical')
            self.instruction = Label(text="Enter a message and the key to be decrypted then press confirm to begin decryption.")
            self.message = TextInput(text="Message", multiline=False)
            self.cont = BoxLayout(orientation='horizontal')
            self.key_field = TextInput(text="Key", multiline=False)
            self.generate = Button(text="Decrypt")
            self.cont.add_widget(self.key_field)
            self.cont.add_widget(self.generate)
            self.result = Label()
            self.validated = False
            self.decryption_screen.add_widget(self.instruction)
            self.decryption_screen.add_widget(self.message)
            self.decryption_screen.add_widget(self.cont)
            self.decryption_screen.add_widget(self.result)

            self.remove_widget(self.selection_screen)
            self.add_widget(self.decryption_screen)

            self.message.bind(on_text_validate=decrypt_message_validate)
            self.key_field.bind(on_text_validate=decrypt_message_validate)
            self.generate.bind(on_press=decrypt)

        self.selection_encryption.bind(on_press=init_encryption_screen)
        self.selection_decryption.bind(on_press=init_decryption_screen)



class Runtime(App):

    def build(self):
        return Main()


if __name__ == '__main__':
    Runtime().run()
