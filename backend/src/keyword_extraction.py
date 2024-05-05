from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.stem import PorterStemmer
import networkx as nx
from collections import Counter
from sqlalchemy.ext.asyncio import AsyncSession
from src.job_posts.models import JobPostKeyword
from src.students.models import StudentKeyword
from sqlmodel import select, delete
from typing import Union
from src.models import ConstrainedId





custom_stopwords = {'candidate', 'experience', 'work', 'working', 'field', 'project', 'technology', 'technologies', 'opportunity', 
                    'area', 'graduate', 'scheme', 'role', 'team', 'skill', 'skills', 'knowledge', 'ability', 'company', 'business', 
                    'service', 'industry', 'year', 'month', 'week', 'day', 'time', 'position', 'level', 'qualification'}

def preprocess_text(
        text: str, 
        allowed_pos: list = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'VBG', 'VB', 'VBD'],
        custom_stopwords: set = custom_stopwords):
    stop_words = set(stopwords.words('english'))
    stop_words.update(custom_stopwords)
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence) for sentence in sentences]
    filtered_words = [[word for word in sentence if word.lower() not in stop_words and word.isalnum()] for sentence in words]
    tagged_words = [pos_tag(sentence) for sentence in filtered_words]
    filtered_pos_words = [[word for word, pos in sentence if pos in allowed_pos] for sentence in tagged_words]
    stemmer = PorterStemmer()
    stemmed_words = [[stemmer.stem(word) for word in sentence] for sentence in filtered_pos_words]
    return stemmed_words


def compute_text_rank(words, window_size=5):
    graph = nx.Graph()
    for sentence in words:
        for i, word in enumerate(sentence):
            for j in range(i+1, min(i+window_size, len(sentence))):
                graph.add_edge(word, sentence[j])
    return nx.pagerank(graph)


def extract_keywords(text):
    # dynamically decide the number of keywords to extract based on the length of the text
    text_len = len(text)
    if text_len < 100:
        top_n = 5
    elif text_len < 300:
        top_n = 10
    else:
        top_n = 15

    words = preprocess_text(text)
    text_rank = compute_text_rank(words)
    return [word for word, score in Counter(text_rank).most_common(top_n)]

async def fetch_keywords(session: AsyncSession, entity_id: Union[str, ConstrainedId], entity_type: str):
    if entity_type == "job_post":
        result = await session.exec(
            select(JobPostKeyword.keyword)
            .where(JobPostKeyword.job_post_id == entity_id))
    else:
        result = await session.exec(
            select(StudentKeyword.keyword)
            .where(StudentKeyword.student_id == entity_id))
    
    return result.all() 

async def create_keywords(session: AsyncSession, entity_id: Union[str, ConstrainedId], entity_type: str, keywords: list[str]):
    if entity_type == "job_post":
        entires = [JobPostKeyword(job_post_id=entity_id, keyword=keyword) for keyword in keywords]
    else:
        entires = [StudentKeyword(student_id=entity_id, keyword=keyword) for keyword in keywords]
    session.add_all(entires)


async def delete_keywords(session: AsyncSession, entity_id: Union[str, ConstrainedId], entity_type: str, keywords: list[str]):
    if entity_type == "job_post":
        await session.exec(
            delete(JobPostKeyword)
            .where(JobPostKeyword.job_post_id == entity_id, JobPostKeyword.keyword.in_(keywords)))
    else:
        await session.exec(
            delete(StudentKeyword)
            .where(StudentKeyword.student_id == entity_id, StudentKeyword.keyword.in_(keywords)))

async def sync_keywords(session: AsyncSession, entity_id: Union[str, ConstrainedId], new_text: str, entity_type: str):
    current_keywords = await fetch_keywords(session, entity_id, entity_type)
    new_keywords = extract_keywords(new_text)

    keywords_to_remove = set(current_keywords) - set(new_keywords)
    keywords_to_add = set(new_keywords) - set(current_keywords)

    if keywords_to_remove:
        await delete_keywords(session, entity_id, entity_type, keywords_to_remove)
    if keywords_to_add:
        await create_keywords(session, entity_id, entity_type, keywords_to_add)
        
        



