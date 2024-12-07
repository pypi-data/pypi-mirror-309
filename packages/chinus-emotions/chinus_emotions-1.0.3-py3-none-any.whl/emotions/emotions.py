import random
import sqlite3


def get_rand_mind():
    with sqlite3.connect('../../data/db/emotions.db') as conn:
        cursor = conn.cursor()

        # PK 개수 확인
        cursor.execute('''SELECT COUNT(id) FROM minds''')
        pk_count = cursor.fetchone()[0]

        # 랜덤 ID 선택
        rand_id = random.randint(1, pk_count)

        # 데이터 조회
        cursor.execute('''
            SELECT word, mean FROM minds WHERE id = ?
        ''', (rand_id,))

        return cursor.fetchone()


def get_rand_feeling():
    with sqlite3.connect('../../data/db/emotions.db') as conn:
        cursor = conn.cursor()

        # PK 개수 확인
        cursor.execute('''SELECT COUNT(id) FROM feelings''')
        pk_count = cursor.fetchone()[0]

        # 랜덤 ID 선택
        rand_id = random.randint(1, pk_count)

        # 데이터 조회
        cursor.execute('''
            SELECT word, mean FROM feelings WHERE id = ?
        ''', (rand_id,))

        return cursor.fetchone()