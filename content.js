const toxicWords = [
    // Hindi & Hinglish Slangs / Toxic Words
    "kutta", "kutti", "kuttay", "kutte", "chutiya", "chutiye", "chutiyapa", 
    "madarchod", "mc", "bhenchod", "bc", "bhosadike", "bhosdike", "bhosdiwaley", 
    "harami", "haraami", "kamina", "kameena", "lauda", "loda", "lund", 
    "gand", "gandu", "bkl", "saala", "saali", "tatti", "bhadwa", "bhadwe", 
    "randi", "jhant", "suar", "ullu", "chinal", "kaminey", "chutiyapan", 
    "chod", "chut", "gaand", "gadha", "gadhe",

    // Punjabi Slangs / Toxic Words
    "kanjar", "kanjri", "chittar", "phuddu", "haraamzada", "ullu da patha", 
    "baimaan", "besharam", "lanti", "lanat", "bakwas", "bhadweya", 

    // English Slangs / Profanity
    "bad", "stupid", "idiot", "dumb", "asshole", "bitch", "bastard", 
    "fuck", "fucking", "fucker", "shit", "bullshit", "ass", "crap", 
    "dick", "pussy", "stfu", "wtf", "loser", "jerk", "moron"
];

document.addEventListener('input', function (event) {
    const target = event.target;
    
    if (target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable)) {
        let text = target.value || target.innerText;
        if (!text) return;

        let words = text.split(' ');
        let modified = false;

        let cleanedWords = words.map(word => {
            // Punctuation saaf karke check karein
            let cleanWord = word.toLowerCase().replace(/[^a-z]/g, '');
            if (toxicWords.includes(cleanWord)) {
                modified = true;
                return '***';
            }
            return word;
        });

        if (modified) {
            let newText = cleanedWords.join(' ');
            if (target.isContentEditable) {
                target.innerText = newText;
            } else {
                target.value = newText;
            }
            
            // Cursor position maintain karne ke liye event dispatch karein
            target.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
});