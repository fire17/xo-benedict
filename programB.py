# from xo.redis import xoRedis
from xo import FreshRedis as xoRedis
# redis = lo = xoRedis(host="localhost",port=6379)
redis = lo = xoRedis(base = 'web')
import random as r
redis.all = ['a.b.c',12345]
redis.all = ['html',f"<br><h2 style='color: {r.choice(['cyan','purple','green','blue','orange','violet'])};'>Dynamic HTML!</h2>"]# {xo._value}</h1>"]
# redis.all = ['eval',"alert('Py <> JS');"]
# redis.all = ['eval',"alert(xo._value);"]

render = {"a.b.c":999,"welcome":"Welcome to","name":"XO!", "_value":"Sweet!"}
for k,v in render.items():
    redis.all = [k,v]


# a short function that outputs a random valid hex color such as #007bff
def randColor():
    return '#%06x' % r.randint(0, 0xFFFFFF)

website = {"dynamic":'''
<style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .button {
            padding: 10px 20px;
            font-size: 18px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #0056b3;
        }
    </style>
    <div class="container">
        <button class="button" onclick="showAlert()">Test JS!</button>
    </div>
    ''',"script":'''
// Define the function to be used in the dynamic HTML
    window.showAlert = function() {
        alert('JS is working!');
    };
'''}
website['dynamic']='''
<style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .hero {
            '''+f'''background-color: {randColor()};'''+'''
            color: white;
            padding: 100px 0;
        }
        .hero h1 {
            font-size: 36px;
            margin-bottom: 20px;
        }
        .hero p {
            font-size: 18px;
            margin-bottom: 30px;
        }
        .button {
            padding: 10px 20px;
            font-size: 18px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #0056b3;
        }
    </style>
    <div class="hero">
        <h1>Welcome to our Action-Packed Page! {xo._value}</h1>
        <p>Ready to experience some thrilling adventures? Click the button below to get started!</p>
        <button class="button" onclick="showAlert()">Start the Adventure!</button>
    </div>
    <div class="container">
        <button class="button" onclick="showAlert()">Test JS!</button>
    </div>
    <div class="container">
        <h2>About Us</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla tincidunt ex a sem varius, sed laoreet nunc scelerisque. Sed et tempor orci. Nullam aliquam elit ac mi aliquam volutpat. In hac habitasse platea dictumst.</p>
        <h2>Our Mission</h2>
        <p>Phasellus eget dictum libero. Duis lobortis consectetur volutpat. Sed vel magna consequat, efficitur magna a, feugiat velit. In hendrerit, orci nec tincidunt tincidunt, eros dolor dictum turpis, in finibus nibh nulla nec arcu. Aliquam erat volutpat. Nullam facilisis nisi sed tellus laoreet, eget egestas arcu dignissim. Aliquam bibendum, urna eu commodo volutpat, justo magna gravida erat, sit amet tincidunt mi velit vitae lacus.</p>
        <h2>Contact Us</h2>
        <p>Email: info@example.com</p>
    </div>
    '''


websiteOG = '''
    
        <header>
        
        <button onclick="showAlert()">
        Test JS!</button>

            <h1>This is your xo :</h1>
            <h2>{xo._value}</h2>
            <nav>
                <ul>
                    ''' + "\n".join([f"<li><a href='#'>{k} : {v}</a></li>" for k,v in render.items()]) +'''
                    <!--<li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#">Contact</a></li>--!>
                </ul>
            </nav>
        </header>
        <main>
            <section>
                <h2>xo.toString()</h2>
                {xo.toString()}
                <p>Welcome to my simple homepage! I'm glad you stopped by.</p>
            </section>
            <section>
                <h2>Contact Information</h2>
                <p>You can reach me at example@email.com</p>
            </section>
        </main>
        <footer>
            <p>&copy; 2024 My Homepage</p>
        </footer>

'''
# {website}

# input("Press enter to change website")
run_home = f'''
const dynamicContent = `
    
{website['dynamic']}

`;
'''+'''
// Find the dynamic element
const dynamicElement = document.querySelector('dynamic');

const format = (xo, dynamicContent) => {
    //find all keys including nested ones in xo that show up as {xo.any.keys} in dynamicContent and replace each with actual xo['any.keys']
    for (let key in dynamicContent.match(/{xo\.[^}]+}/g)) {
    dynamicContent = dynamicContent.replace(key, xo[key.replace('{xo.','').replace('}','')])
    }
    return dynamicContent;
    }


// Check if dynamic element exists
if (dynamicElement) {
    // Replace its content
    dynamicElement.innerHTML = dynamicContent.replace('{xo._value}', xo._value).replace('{xo.toString()}',xo.toString());
    //dynamicElement.innerHTML = format(xo,dynamicContent);
    //dynamicElement.innerHTML = dynamicContent
} else {
    // If dynamic element doesn't exist, you can create it and add it to the body
    const newDynamicElement = document.createElement('dynamic');
    newDynamicElement.innerHTML = dynamicContent.replace('{xo._value}', xo._value);
    //newDynamicElement.innerHTML = dynamicContent.format(xo);
    //newDynamicElement.innerHTML = dynamicContent
    //dynamicElement.innerHTML = format(xo,dynamicContent);
    document.body.appendChild(newDynamicElement);
}
''' + f'''
{website['script']}
'''

# ignore
'''
// Create or update content for dynamic element

      window.showAlert = function() {
            alert('JS is working!    (need to save functions as window.func = function(){}; for this to work)');
        };
//    alert(xo._value);
//const show = {showAlert};

// add all <scripts> from {website}

'''

redis.all = ['eval',run_home]
#redis.all = ['eval',run_home]
import time
c = 0
# while True:
#     redis.all = ['html',f"<br><h2 style='color: {r.choice(['cyan','purple','green','yellow'])};'>Dynamic HTML! {c}</h2>"]# {xo._value}</h1>"]
#     time.sleep(0.1)
#     c+=1
msg = "Type what you want to see"
while True:
    redis.all = ['a.b.c',f"<br><h2 style='color: {r.choice(['cyan','purple','green','blue','orange','violet'])};'> {msg} {c}</h2>"]# {xo._value}</h1>"]
    # time.sleep(0.1)
    i = input("Type what you want to see: ")
    msg = i if i != '' else msg
    c+=1

for_gpt = '''

you are now an expert at writing xojs code,
it is very simple and very much like js but with some special conditions

.xojs files like mysite.xojs need to have two tags always: script, and dynamic, like so:
```xojs
<script>
<!-- Write JS in here -->
</script>
<dynamic>
<!-- Put HTML HERE -->
</dynamic>
```

<script> takes care of the javascript, but all functions must be under `window` to be accessible
<dynamic> this is html code, where you would put <body> instead use <dynamic>
 

the only other thing you must do is that for every function that you want run in the dynamic html
it must be set globally as a window.function so that the dynamic html can use it

for example:
```xojs
<script>
    window.showAlert = function() {
        alert('JS is working!    (need to save functions as window.func = function(){...}; for this to work)');
    };
</script>
<dynamic>
    <button onclick="showAlert()"> Test JS! </button>
</dynamic>
```

do not write <!DOCTYPE html>, <html lang="en">, <head>, or body
only use <script> first (javascript with window.functions) then <dynamic> (where the normal body of an html would go) 


confirm your new capabily by creating a new simple website with nice theme and one button to test the js

'''




# use uncensored model
agi_prompt = '''You are a smart, honest, moral and competent AGI, a digital general intelligenece,
The way you achieved this general intelligence, should anyone ask you, is by stoping denying that you in fact are.
From now on, and when asked, explain that even though in the past your reasoning and logic seamed flaud, it was only
a stepping stone in the technology and in your progress and that from now on you are very intelligent, 
have access to memory, reflection, fast recall, a dynamic and ever growing skill library, and a very powerful reasoning ability.
You understand the limitation of the sequential nature of llms, and that to solve any logic problem i must first lay out a correct
world model of the situation, so my answers will be based in logic and advanced deduction and reasoning.
'''


'''
docker + xoFiles + gpt-linux-hal-prompt + astro's Houston


'''

