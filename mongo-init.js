db = db.getSiblingDB('image_moderation');

db.tokens.insertOne({
    token: "admin",
    isAdmin: true,
    createdAt: new Date()
});
