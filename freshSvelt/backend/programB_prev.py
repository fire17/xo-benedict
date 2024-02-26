from xo.redis import xoRedis
redis = lo = xoRedis(host="localhost",port=6379)
import random as r
redis.all = ['a.b.c',12345]
redis.all = ['_html',f"<br><h1 style='color: {r.choice(['cyan','purple','green','yellow'])};'>Welcome to XO!</h1>"]# {xo._value}</h1>"]
# redis.all = ['eval',"alert('Py <> JS');"]
# redis.all = ['eval',"alert(xo._value);"]

render = {"a.b.c":999,"welcome":"Welcome to","name":"XO!", "_value":"Sweet!"}
for k,v in render.items():
    redis.all = [k,v]

website = '''
    
        <header>
        
        <button onclick="showAlert()">
        Click me!</button>

            <h1>This is your xo's dir: {xo._value} @@!!!@@</h1>
            <nav>
                <ul>
                    ''' + "\n".join([f"<li><a href='#'>{k} : {v}</a></li>" for k,v in render.items()]) +'''
                    <li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#">Contact</a></li>
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

# input("Press enter to change website")
run_home = f'''
const dynamicContent = `
    
{website}

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
'''+'''
// Create or update content for dynamic element

      window.showAlert = function() {
            alert('yooooooo');
        };
    alert(xo._value);
//const show = {showAlert};

// add all <scripts> from {website}

'''

redis.all = ['eval',run_home]
#redis.all = ['eval',run_home]
