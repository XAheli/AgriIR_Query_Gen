"""
Database module for storing statements and pairs
"""
import sqlite3
import pandas as pd
from datetime import datetime
import config

class StatementDatabase:
    def __init__(self, db_path=config.DATABASE_PATH):
        self.db_path = db_path
        self.create_tables()
    
    def create_tables(self):
        """Create necessary database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Statements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                source_url TEXT,
                author TEXT,
                publication_date TEXT,
                topic TEXT,
                document_id TEXT,
                created_at TEXT,
                UNIQUE(text, source_url)
            )
        ''')
        
        # Statement pairs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statement_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                statement_a_id INTEGER,
                statement_b_id INTEGER,
                similarity_score REAL,
                same_source BOOLEAN,
                relationship_label TEXT,
                inconsistency_subtype TEXT,
                created_at TEXT,
                FOREIGN KEY (statement_a_id) REFERENCES statements(id),
                FOREIGN KEY (statement_b_id) REFERENCES statements(id),
                UNIQUE(statement_a_id, statement_b_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_statement(self, text, source_url, author=None, topic=None, document_id=None):
        """Insert a statement into the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO statements (text, source_url, author, topic, document_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (text, source_url, author, topic, document_id, datetime.now().isoformat()))
            conn.commit()
            statement_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Statement already exists
            cursor.execute('SELECT id FROM statements WHERE text=? AND source_url=?', 
                         (text, source_url))
            statement_id = cursor.fetchone()[0]
        
        conn.close()
        return statement_id
    
    def insert_pair(self, statement_a_id, statement_b_id, similarity_score, same_source=True):
        """Insert a statement pair"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO statement_pairs 
                (statement_a_id, statement_b_id, similarity_score, same_source, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (statement_a_id, statement_b_id, similarity_score, same_source, 
                  datetime.now().isoformat()))
            conn.commit()
            pair_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            pair_id = None
        
        conn.close()
        return pair_id
    
    def get_all_statements(self):
        """Retrieve all statements as DataFrame"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM statements", conn)
        conn.close()
        return df
    
    def get_all_pairs(self):
        """Retrieve all statement pairs with full text"""
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT 
                p.id,
                s1.text as statement_a,
                s2.text as statement_b,
                s1.source_url as source_a,
                s2.source_url as source_b,
                s1.author as author_a,
                s2.author as author_b,
                s1.topic as topic_a,
                s2.topic as topic_b,
                p.similarity_score,
                p.same_source,
                p.relationship_label,
                p.inconsistency_subtype
            FROM statement_pairs p
            JOIN statements s1 ON p.statement_a_id = s1.id
            JOIN statements s2 ON p.statement_b_id = s2.id
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
