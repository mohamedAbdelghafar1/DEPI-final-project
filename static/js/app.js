const API_URL = '/';

// State
let currentPage = 1;
let currentProducts = [];
let currentUser = 4;
let activeTab = 'hybrid';

// DOM Elements
const productList = document.getElementById('productList');
const productModal = document.getElementById('productModal');
const searchInput = document.getElementById('productSearch');
const searchBtn = document.getElementById('searchBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const pageInfo = document.getElementById('pageInfo');
const userSelect = document.getElementById('userSelect');
const tabBtns = document.querySelectorAll('.tab-btn');
const recList = document.getElementById('recList');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
    fetchUserRecommendations();

    // Event Listeners
    searchBtn.addEventListener('click', () => searchProducts(searchInput.value));
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchProducts(searchInput.value);
    });

    prevBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            fetchProducts(currentPage);
        }
    });

    nextBtn.addEventListener('click', () => {
        currentPage++;
        fetchProducts(currentPage);
    });

    document.querySelector('.close-modal').addEventListener('click', () => {
        productModal.classList.remove('visible');
    });

    userSelect.addEventListener('change', (e) => {
        currentUser = e.target.value;
        fetchUserRecommendations();
    });

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeTab = btn.dataset.tab;
            fetchUserRecommendations();
        });
    });

    // Check health
    fetch('/health')
        .then(res => res.json())
        .then(data => console.log('API Status:', data.status));
});

// API Calls
async function fetchProducts(page = 1) {
    try {
        const res = await fetch(`${API_URL}products?page=${page}&limit=12`);
        const data = await res.json();
        renderProducts(data.products, productList);
        updatePagination(data.page, data.total);
    } catch (err) {
        console.error('Error fetching products:', err);
    }
}

async function searchProducts(query) {
    if (!query.trim()) return fetchProducts(1);
    try {
        const res = await fetch(`${API_URL}products/search?q=${encodeURIComponent(query)}&limit=12`);
        const data = await res.json();
        renderProducts(data.products, productList);
        // Hide pagination for search results
        pageInfo.textContent = `Search results: ${data.products.length}`;
        prevBtn.disabled = true;
        nextBtn.disabled = true;
    } catch (err) {
        console.error('Error searching:', err);
    }
}

async function fetchUserRecommendations() {
    recList.innerHTML = '<p>Loading recommendations...</p>';
    try {
        let endpoint = '';
        if (activeTab === 'collaborative') {
            endpoint = `recommendations/collaborative?user_id=${currentUser}&top_n=8`;
        } else {
            // For hybrid, we need a product context. 
            // In a real app, this would be user's last viewed item or similar.
            // Here we'll use a default popular item or the first item from their collaborative list
            const collabRes = await fetch(`${API_URL}recommendations/collaborative?user_id=${currentUser}&top_n=1`);
            const collabData = await collabRes.json();
            const seedProduct = collabData.recommendations[0]?.name || "OPI Nail Polish, Strawberry Margarita, 0.5 Fl Oz";

            endpoint = `recommendations/hybrid?user_id=${currentUser}&product_name=${encodeURIComponent(seedProduct)}&top_n=8`;
        }

        const res = await fetch(`${API_URL}${endpoint}`);
        const data = await res.json();
        renderProducts(data.recommendations, recList);
    } catch (err) {
        console.error('Error fetching recommendations:', err);
        recList.innerHTML = '<p>Error loading recommendations.</p>';
    }
}

async function fetchContentRecommendations(productName) {
    try {
        const res = await fetch(`${API_URL}recommendations/content-based?product_name=${encodeURIComponent(productName)}&top_n=5`);
        const data = await res.json();
        renderSimilarProducts(data.recommendations);
    } catch (err) {
        console.error('Error fetching similar products:', err);
    }
}

// Rendering
function renderProducts(products, container) {
    container.innerHTML = '';
    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <img src="${product.image_url || ''}" class="product-img" alt="${product.name}" onerror="this.onerror=null; this.src='https://picsum.photos/seed/${product.product_id}/300/300';">
            <div class="product-details">
                <div class="product-brand">${product.brand}</div>
                <div class="product-title">${product.name}</div>
                <div class="product-rating">
                    <span>★ ${product.rating || '0.0'}</span>
                    <span class="rating-count">(${product.reviews_count || 0})</span>
                </div>
            </div>
        `;
        card.addEventListener('click', () => showProductDetails(product));
        container.appendChild(card);
    });

    if (products.length === 0) {
        container.innerHTML = '<p>No products found.</p>';
    }
}

function renderSimilarProducts(products) {
    const container = document.getElementById('similarProductsList');
    container.innerHTML = '';
    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'rec-card';
        card.innerHTML = `
            <img src="${product.image_url || ''}" alt="${product.name}" onerror="this.onerror=null; this.src='https://picsum.photos/seed/${product.product_id || product.name.length}/200/200';">
            <h4>${product.name}</h4>
        `;
        card.addEventListener('click', () => showProductDetails(product));
        container.appendChild(card);
    });
}

function showProductDetails(product) {
    document.getElementById('detailImage').src = product.image_url || 'https://via.placeholder.com/400';
    document.getElementById('detailName').textContent = product.name;
    document.getElementById('detailBrand').textContent = product.brand;
    document.getElementById('detailRating').textContent = `★ ${product.rating || 0} (${product.reviews_count || 0} reviews)`;
    document.getElementById('detailDescription').textContent = product.description || 'No description available.';

    productModal.classList.add('visible');

    fetchContentRecommendations(product.name);
}

function updatePagination(page, total) {
    pageInfo.textContent = `Page ${page}`;
    prevBtn.disabled = page === 1;
    // Simple check for next button, strictly calculating total pages would be better
    nextBtn.disabled = false;
}
