import os
import psycopg2
import bcrypt

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=tc_store')
connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()

# insert some sample products
cursor.execute("""
    INSERT INTO toy (name, image_url_1, image_url_2, qty, price) VALUES
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s)
""",
    (
        'Dark Leo Prime', '/static/assets/cba17704c72747e282076af4d2c2398e_Large.png','/static/assets/835ef8f40f9149fcab4dd21d84514f2b_Large.png', 10, 300,
        'Bumblebee', '/static/assets/009aee53451d46b3b9b9021685f9a76f_Large.png','/static/assets/45ad22044568465ca3ee278ed9951355_Large.png', 10, 45,
        'Kickback', '/static/assets/99c7cce2c24548ca8b2310d8710f00a8_Large.png','/static/assets/06b3abaaa33b4d13b519967d9fa06fae_Large.png', 10, 45,
        'Galvatron', '/static/assets/9caa644c55ce431eae9f61e3debcfc2b_Large.png','/static/assets/f7dab7e3fc6c4f8f88dd224730046dc2_Large.png', 10, 58,
        'DK-2 Guard', '/static/assets/a0d808bcb2f342c7910b75489237d021_Large.png','/static/assets/fec9abb635fb44889b9c2c65873ee4aa_Large.png', 10, 50,
        'Thundercracker', '/static/assets/48441c62099d4ade89266e2b4da56e1f_Large.png','/static/assets/23777c9738a74902b2b2c6c02e0488d2_Large.png', 10, 58,
        'Knock', '/static/assets/2523439c26814372b6a84e0f16c2beec_Large.png','/static/assets/26fb27d05fea48bb89310430208230ff_Large.png', 10, 45,
        'Takara Optimus Prime', '/static/assets/79a018950e314ecd9ec99775d5d36b79_Large.png','/static/assets/d269050e36824fe8922dcea2240478d5_Large.png', 10, 158,
        'Arcee', '/static/assets/0a1cebe7922844848bd2158d2c868d7e_Large.png','/static/assets/77071c0d385642d5b6414f9e522005c1_Large.png', 10, 58,
        'WFC Senator Crosscut', '/static/assets/588704abc92c4c4a866826fc9549dcbc_Large.png','/static/assets/d55bbfa27ef449eaaf72caa8cdad3e02_Large.png', 10, 158,
        'WFC Nightbird Shadow', '/static/assets/3c8d8e8ce9f44db796711f45e2d6f6bb_Large.png','/static/assets/fe434010b9634d0d8ca1c66c35f626e2_Large.png', 10, 358,
        'Takara Megatron', '/static/assets/ed6ac4d60b7046a680d23dcf53bca480_Large.png','/static/assets/d5b8c1e83dac4fa09ce6fd30bee165e9_Large.png', 10, 158
    )
)
connection.commit()

# insert some user with hashed passwords
# hashed passwords make it harder for hackers to gain access to our web application should they somehow can read our users table
cursor.execute("""
    INSERT INTO users (username, password_hash, address) VALUES
    (%s, %s, %s),
    (%s, %s, %s),
    (%s, %s, %s)
""",
    (
      "Anson", bcrypt.hashpw(b"letmein", bcrypt.gensalt()).decode(),'U1/ 88 Back St, Sydney 2000',
      "Jack", bcrypt.hashpw(b"letmein", bcrypt.gensalt()).decode(),'U2/ 86 Front St, Sydney 2000',
      "Mary", bcrypt.hashpw(b"letmein", bcrypt.gensalt()).decode(),'U16/ 18 John St, Sydney 2000'
    )
)
connection.commit()

