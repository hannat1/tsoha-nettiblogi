CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    visible BOOLEAN DEFAULT TRUE
);
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT, 
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP, 
    visible BOOLEAN DEFAULT TRUE
);
CREATE TABLE followings (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER REFERENCES users,
    followed_id INTEGER REFERENCES users,
    visible BOOLEAN DEFAULT TRUE
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    user_id INTEGER REFERENCES users,
    content TEXT,
    sent_at TIMESTAMP, 
    visible BOOLEAN DEFAULT TRUE
);
CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    user_id INTEGER REFERENCES users,
    visible BOOLEAN DEFAULT TRUE
);


