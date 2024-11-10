// Register User
function validatePassword(password) {
    const minLength = password.length >= 7;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    return minLength && hasUppercase && hasLowercase;
}

// Register User
document.getElementById("registrationForm").onsubmit = async (event) => {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const passwordMessage = document.getElementById("passwordMessage");

    // Validate password
    if (!validatePassword(password)) {
        passwordMessage.textContent = "Password must be at least 7 characters, with at least one uppercase and one lowercase letter.";
        return;
    } else {
        passwordMessage.textContent = "";
    }

    // Hash password with SHA-256
    const hashedPassword = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(password));
    const passwordHashHex = Array.from(new Uint8Array(hashedPassword))
        .map(b => b.toString(16).padStart(2, "0"))
        .join("");

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password: passwordHashHex })
    });

    const result = await response.json();
    document.getElementById("registrationMessage").innerText = result.message;
};

// Search Products
// Search Products and Display as Cards
async function searchProducts() {
    const query = document.getElementById("searchQuery").value;
    const productDisplay = document.getElementById("productDisplay");

    // Clear previous results
    productDisplay.innerHTML = '';

    // Fetch products from backend
    const response = await fetch(`/search_products?query=${query}`);
    const results = await response.json();

    if (results.length === 0) {
        productDisplay.innerHTML = '<p>No products found</p>';
        return;
    }

    // Generate product cards
    results.forEach(product => {
        const card = document.createElement('div');
        card.classList.add('product-card');
        
        // Product name
        const name = document.createElement('h3');
        name.textContent = product.name;
        card.appendChild(name);

        // Product description
        const description = document.createElement('p');
        description.textContent = product.description;
        card.appendChild(description);

        // Product category
        const category = document.createElement('p');
        category.textContent = `Category: ${product.category}`;
        card.appendChild(category);

        // Product price
        const price = document.createElement('p');
        price.classList.add('price');
        price.textContent = `$${product.price.toFixed(2)}`;
        card.appendChild(price);

        // Append card to product display
        productDisplay.appendChild(card);
    });
}


// Get Recommendations
async function getRecommendations() {
    const userId = document.getElementById("recommendationUserId").value;
    const response = await fetch(`/recommend/${userId}`);
    const recommendations = await response.json();

    const recommendationList = document.getElementById("recommendationList");
    recommendationList.innerHTML = '';
    if (recommendations.message) {
        recommendationList.innerText = recommendations.message;
    } else {
        recommendations.forEach(product => {
            const item = document.createElement('li');
            item.innerText = `${product.name} - ${product.description} - $${product.price}`;
            recommendationList.appendChild(item);
        });
    }
}
// Register new user
async function register() {
    const username = document.getElementById("registerUsername").value;
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });
    
    const result = await response.json();
    alert(result.message);
}

// Login user
async function login() {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    const result = await response.json();
    if (response.ok) {
        showMainSite();
    } else {
        alert(result.message);
    }
}

// Check if user is logged in on page load
async function checkLoginStatus() {
    const response = await fetch('/is_logged_in');
    const result = await response.json();
    if (result.logged_in) {
        showMainSite();
    }
}

// Show main site and hide auth section
function showMainSite() {
    document.getElementById("authSection").style.display = "none";
    document.getElementById("mainSite").style.display = "block";
}

// Logout user
async function logout() {
    const response = await fetch('/logout', { method: 'POST' });
    const result = await response.json();
    alert(result.message);
    document.getElementById("authSection").style.display = "block";
    document.getElementById("mainSite").style.display = "none";
}

// Run check on page load
checkLoginStatus();
