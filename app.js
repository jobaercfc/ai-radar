let brief = null;
let readItems = new Set(JSON.parse(localStorage.getItem('readItems') || '[]'));
let bookmarks = new Set(JSON.parse(localStorage.getItem('bookmarks') || '[]'));
let currentSectionIndex = 0;
let allSections = [];
let sortNewestFirst = localStorage.getItem('sortOrder') !== 'oldest';
let activeSourceFilter = 'rss';

// Source type labels
const SOURCE_TYPES = [
    { key: 'all', label: 'All' },
    { key: 'rss', label: 'RSS' },
    { key: 'hackernews', label: 'Hacker News' },
    { key: 'github', label: 'GitHub' },
    { key: 'reddit', label: 'Reddit' },
    { key: 'arxiv', label: 'arXiv' },
    { key: 'blog', label: 'Blogs' },
];

// Theme management
const theme = localStorage.getItem('theme') || 'dark';
if (theme === 'light') document.body.classList.add('light-mode');

async function loadBrief() {
    try {
        const res = await fetch('data/latest.json');
        brief = await res.json();

        // Propagate read_time_minutes from all_items to section items by URL
        if (brief.all_items) {
            const readTimes = {};
            brief.all_items.forEach(it => {
                if (it.read_time_minutes) readTimes[it.url] = it.read_time_minutes;
            });
            brief.sections.forEach(sec => {
                sec.items.forEach(item => {
                    if (!item.read_time_minutes && readTimes[item.url]) {
                        item.read_time_minutes = readTimes[item.url];
                    }
                });
            });
        }

        render();
    } catch (e) {
        document.getElementById('loading').innerHTML = '<p class="text-red-400">Failed to load</p>';
    }
}

function calculateReadingTime(text) {
    const wordsPerMinute = 200;
    const words = text.trim() ? text.split(/\s+/).length : 0;
    const totalSeconds = Math.round((words / wordsPerMinute) * 60);
    if (totalSeconds < 60) {
        const rounded = Math.max(15, Math.round(totalSeconds / 15) * 15);
        return { display: `~${rounded} sec`, minutes: 0 };
    }
    const mins = Math.ceil(totalSeconds / 60);
    return { display: `${mins} min`, minutes: mins };
}

function render() {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('dateDisplay').textContent = new Date(brief.date).toLocaleDateString('en-US', {weekday:'long', year:'numeric', month:'long', day:'numeric'});
    // Make headline clickable — find the item whose title best matches the headline
    const headlineEl = document.getElementById('headline');
    const headlineWords = new Set(brief.headline.toLowerCase().replace(/[^\w\s]/g, '').split(/\s+/).filter(w => w.length > 3));
    let bestUrl = null, bestScore = 0;
    brief.sections.forEach(sec => {
        sec.items.forEach(item => {
            const titleWords = item.title.toLowerCase().replace(/[^\w\s]/g, '').split(/\s+/);
            const score = titleWords.filter(w => headlineWords.has(w)).length;
            if (score > bestScore) { bestScore = score; bestUrl = item.url; }
        });
    });
    if (bestUrl) {
        headlineEl.innerHTML = `<a href="${bestUrl}" target="_blank" style="text-decoration:none;color:inherit" class="hover:text-purple-400">${brief.headline}</a>`;
    } else {
        headlineEl.textContent = brief.headline;
    }
    document.getElementById('lastUpdated').textContent = new Date(brief.generated_at).toLocaleString();

    // Calculate total reading time
    let totalMinutes = 0;
    brief.sections.forEach(sec => {
        sec.items.forEach(item => {
            if (item.read_time_minutes) {
                totalMinutes += item.read_time_minutes;
            } else {
                const text = (item.summary || '') + ' ' + (item.why_it_matters || '');
                totalMinutes += calculateReadingTime(text).minutes;
            }
        });
    });
    document.getElementById('totalReadingTime').textContent = `${totalMinutes || '< 1'} min`;

    // Sort items by published date
    sortAllItems();

    allSections = brief.sections.map(s => s.id);
    if (brief.all_items && brief.all_items.length) allSections.push('all_news');

    // Render tabs
    const tabsEl = document.getElementById('tabs');
    tabsEl.innerHTML = '';
    tabsEl.classList.remove('hidden');

    brief.sections.forEach((sec, i) => {
        const tab = document.createElement('div');
        tab.className = 'tab py-3 px-4 inline-block';
        if (i === 0) tab.classList.add('active');

        let secMinutes = 0;
        sec.items.forEach(it => {
            secMinutes += it.read_time_minutes || calculateReadingTime((it.summary || '') + ' ' + (it.why_it_matters || '')).minutes;
        });
        const secTimeLabel = secMinutes ? `${secMinutes} min` : '< 1 min';
        tab.innerHTML = `<span class="text-xl mr-2">${sec.emoji}</span>${sec.title} <span class="text-xs bg-gray-800 px-2 py-1 rounded ml-2">${sec.items.length}</span> <span class="reading-time ml-2">⏱️ ${secTimeLabel}</span>`;
        tab.onclick = () => switchTab(sec.id, i);
        tabsEl.appendChild(tab);
    });

    if (brief.all_items && brief.all_items.length) {
        const allTab = document.createElement('div');
        allTab.className = 'tab py-3 px-4 inline-block';
        allTab.innerHTML = `<span class="text-xl mr-2">📰</span>All News <span class="text-xs bg-gray-800 px-2 py-1 rounded ml-2">${brief.all_items.length}</span>`;
        allTab.onclick = () => switchTab('all_news', allSections.length - 1);
        tabsEl.appendChild(allTab);
    }

    // Render content
    const contentEl = document.getElementById('content');
    contentEl.innerHTML = '';
    contentEl.classList.remove('hidden');

    brief.sections.forEach((sec, i) => {
        const div = document.createElement('div');
        div.id = `sec-${sec.id}`;
        div.className = i === 0 ? '' : 'hidden';
        div.innerHTML = `<h2 class="text-2xl font-bold mb-6"><span class="text-3xl mr-2">${sec.emoji}</span>${sec.title}</h2>` + sec.items.map((item, idx) => renderItem(item, idx)).join('');
        contentEl.appendChild(div);
    });

    if (brief.all_items && brief.all_items.length) {
        const allDiv = document.createElement('div');
        allDiv.id = 'sec-all_news';
        allDiv.className = 'hidden';

        // Build source filter chips + sort button
        const chipsHtml = SOURCE_TYPES.map(s =>
            `<button class="source-chip ${s.key === activeSourceFilter ? 'active' : ''}" data-filter="${s.key}" onclick="setSourceFilter('${s.key}')">${s.label}</button>`
        ).join('');
        const sortLabel = sortNewestFirst ? 'Newest first ↓' : 'Oldest first ↑';

        allDiv.innerHTML = '<h2 class="text-2xl font-bold mb-6">📰 All News</h2>'
            + '<input type="text" id="search" placeholder="Search..." class="w-full mb-3 bg-gray-900 border border-gray-700 rounded px-4 py-2" oninput="filterAllNews()">'
            + `<div class="flex gap-2 mb-4 flex-wrap items-center" id="sourceChips">${chipsHtml}<button class="sort-btn ml-auto" onclick="toggleSort()" id="sortBtn">${sortLabel}</button></div>`
            + brief.all_items.map((item, idx) => renderItem(item, idx, true)).join('');
        contentEl.appendChild(allDiv);
    }

    document.getElementById('footer').classList.remove('hidden');
}

function renderItem(item, idx, showFeatured = false) {
    const isRead = readItems.has(item.url);
    const isBookmarked = bookmarks.has(item.url);
    const featured = showFeatured && brief.sections.some(s => s.items.some(i => i.url === item.url));
    const readTime = item.read_time_minutes
        ? `${item.read_time_minutes} min`
        : calculateReadingTime((item.summary || '') + ' ' + (item.why_it_matters || '')).display;
    const sourceAttr = showFeatured ? ` data-source="${item.source_type || ''}"` : '';

    return `
        <div class="card p-6 rounded-lg mb-4 ${isRead ? 'read' : ''} ${isBookmarked ? 'bookmarked' : ''}" data-url="${item.url}" data-idx="${idx}"${sourceAttr}>
            <div class="flex justify-between items-start mb-3">
                <h3 class="text-xl font-semibold flex-1">
                    <a href="${item.url}" target="_blank" class="hover:text-purple-400">${item.title}</a>
                </h3>
                <div class="flex gap-2 ml-4">
                    <button onclick="toggleRead('${item.url}')" class="text-xs px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded">${isRead ? '✓' : 'Read'}</button>
                    <button onclick="toggleBookmark('${item.url}')" class="text-xs px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded">${isBookmarked ? '★' : '☆'}</button>
                </div>
            </div>
            <div class="flex gap-2 mb-3 flex-wrap">
                <span class="text-xs bg-gray-800 px-3 py-1 rounded">${item.source}</span>
                ${item.published ? `<span class="text-xs text-gray-500">🕐 ${new Date(item.published).toLocaleDateString()}</span>` : ''}
                <span class="reading-time">⏱️ ${readTime} read</span>
                ${featured ? '<span class="text-xs bg-purple-900 px-3 py-1 rounded">✨ Featured</span>' : ''}
            </div>
            <p class="text-gray-300 leading-relaxed">${item.summary || ''}</p>
            ${item.why_it_matters ? `<div class="mt-3 p-3 bg-purple-900/20 border-l-2 border-purple-500 rounded"><p class="text-sm text-purple-200"><strong>Why it matters:</strong> ${item.why_it_matters}</p></div>` : ''}
        </div>
    `;
}

function switchTab(id, index) {
    currentSectionIndex = index;
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab')[index].classList.add('active');
    document.querySelectorAll('[id^="sec-"]').forEach(s => s.classList.add('hidden'));
    document.getElementById(`sec-${id}`).classList.remove('hidden');
    window.scrollTo(0, 0);

    // Apply source filter when switching to All News
    if (id === 'all_news') {
        filterAllNews();
    }
}

function toggleRead(url) {
    if (readItems.has(url)) readItems.delete(url);
    else readItems.add(url);
    localStorage.setItem('readItems', JSON.stringify([...readItems]));
    document.querySelector(`[data-url="${url}"]`).classList.toggle('read');
}

function toggleBookmark(url) {
    if (bookmarks.has(url)) bookmarks.delete(url);
    else bookmarks.add(url);
    localStorage.setItem('bookmarks', JSON.stringify([...bookmarks]));
    document.querySelector(`[data-url="${url}"]`).classList.toggle('bookmarked');
}

function toggleTheme() {
    document.body.classList.toggle('light-mode');
    const isLight = document.body.classList.contains('light-mode');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    document.getElementById('themeIcon').textContent = isLight ? '☀️' : '🌙';
}

function prevSection() {
    if (currentSectionIndex > 0) {
        const newIndex = currentSectionIndex - 1;
        switchTab(allSections[newIndex], newIndex);
    }
}

function nextSection() {
    if (currentSectionIndex < allSections.length - 1) {
        const newIndex = currentSectionIndex + 1;
        switchTab(allSections[newIndex], newIndex);
    }
}

function scrollToTop() {
    window.scrollTo({top: 0, behavior: 'smooth'});
}

function setSourceFilter(type) {
    activeSourceFilter = type;
    document.querySelectorAll('.source-chip').forEach(chip => {
        chip.classList.toggle('active', chip.dataset.filter === type);
    });
    filterAllNews();
}

function filterAllNews() {
    const searchEl = document.getElementById('search');
    const q = searchEl ? searchEl.value.toLowerCase() : '';
    document.querySelectorAll('#sec-all_news .card').forEach(c => {
        const matchesSearch = !q || c.textContent.toLowerCase().includes(q);
        const matchesSource = activeSourceFilter === 'all' || c.dataset.source === activeSourceFilter;
        c.style.display = (matchesSearch && matchesSource) ? 'block' : 'none';
    });
}

function sortByDate(items) {
    return items.sort((a, b) => {
        const da = a.published ? new Date(a.published).getTime() : 0;
        const db = b.published ? new Date(b.published).getTime() : 0;
        return sortNewestFirst ? db - da : da - db;
    });
}

function sortAllItems() {
    brief.sections.forEach(sec => sortByDate(sec.items));
    if (brief.all_items) sortByDate(brief.all_items);
}

function toggleSort() {
    sortNewestFirst = !sortNewestFirst;
    localStorage.setItem('sortOrder', sortNewestFirst ? 'newest' : 'oldest');

    // Re-sort and re-render only All News cards
    sortAllItems();
    const allDiv = document.getElementById('sec-all_news');
    if (allDiv) {
        // Remove old cards, keep header + search + chips row
        allDiv.querySelectorAll('.card').forEach(c => c.remove());
        allDiv.insertAdjacentHTML('beforeend', brief.all_items.map((item, idx) => renderItem(item, idx, true)).join(''));
        filterAllNews();
    }
    document.getElementById('sortBtn').textContent = sortNewestFirst ? 'Newest first ↓' : 'Oldest first ↑';
}

function showStats() {
    const total = (brief.all_items || []).length;
    const read = readItems.size;
    const bookmarked = bookmarks.size;
    const readPercent = total > 0 ? Math.round((read / total) * 100) : 0;

    document.getElementById('statsContent').innerHTML = `
        <div class="grid grid-cols-2 gap-4 text-center mb-6">
            <div><div class="text-3xl font-bold text-purple-400">${total}</div><div class="text-sm text-gray-400">Total</div></div>
            <div><div class="text-3xl font-bold text-green-400">${read}</div><div class="text-sm text-gray-400">Read (${readPercent}%)</div></div>
            <div><div class="text-3xl font-bold text-yellow-400">${bookmarked}</div><div class="text-sm text-gray-400">Bookmarked</div></div>
            <div><div class="text-3xl font-bold text-blue-400">${document.getElementById('totalReadingTime').textContent}</div><div class="text-sm text-gray-400">Est. Time</div></div>
        </div>
        <div class="w-full bg-gray-700 rounded-full h-2">
            <div class="bg-green-500 h-2 rounded-full" style="width: ${readPercent}%"></div>
        </div>
        <p class="text-center text-sm text-gray-400 mt-2">Reading Progress</p>
    `;
    document.getElementById('statsModal').classList.add('show');
}

function showHelp() {
    document.getElementById('helpModal').classList.add('show');
}

function closeModals() {
    document.querySelectorAll('.modal').forEach(m => m.classList.remove('show'));
}

function exportMD() {
    let md = `# AI Radar - ${brief.date}\n\n${brief.headline}\n\n`;
    brief.sections.forEach(sec => {
        md += `## ${sec.emoji} ${sec.title}\n\n`;
        sec.items.forEach(item => {
            md += `### ${item.title}\n${item.summary}\n[Read more](${item.url})\n\n`;
        });
    });
    const blob = new Blob([md], {type: 'text/markdown'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ai-radar-${brief.date}.md`;
    a.click();
}

document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModals();
    if (e.key === '?') showHelp();
    if (e.key === 's') showStats();
    if (e.key === 'e') exportMD();
    if (e.key === 't') toggleTheme();
    if (e.key === 'Home') scrollToTop();
    if (e.key === 'ArrowLeft') prevSection();
    if (e.key === 'ArrowRight') nextSection();
});

window.addEventListener('scroll', () => {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    const p = (window.scrollY / h) * 100;
    document.getElementById('progressFill').style.width = p + '%';
});

loadBrief();
