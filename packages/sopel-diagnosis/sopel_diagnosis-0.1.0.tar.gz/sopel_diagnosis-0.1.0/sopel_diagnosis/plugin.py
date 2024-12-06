# coding=utf8
"""sopel-diagnosis

A silly Sopel plugin to diagnose your friends with random mental disorders.

(Just for fun! NOT medical advice.)
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import itertools
import random

from sopel import plugin


@plugin.command('diagnose')
def hello_world(bot, trigger):
    """Much scientific, very medically sound, wow."""
    message = "{verb_phrase} {condition}."
    patient = trigger.group(2)

    if patient is None:
        patient = trigger.nick

    condition = random.choice(CONDITIONS)
    verb_phrase = next(VERB_PHRASES).format(patient=patient)

    bot.say(message.format(verb_phrase=verb_phrase, condition=condition))


# curated list based on https://en.wikipedia.org/wiki/List_of_mental_disorders
# some entries removed, modified, or replaced to fit the plugin's tone better
DSM_AND_ICD_CONDITIONS = [
    # Anxiety disorders
    'generalized anxiety',
    'separation anxiety',
    'social anxiety'
    'agoraphobia',
    'selective mutism',

    # Dissociative disorders
    'dissociative identity disorder',
    'psychogenic amnesia',
    'depersonalization-derealization disorder',
    'dissociative fugue',

    # Mood disorders
    'disruptive mood dysregulation disorder',
    'major depressive disorder',
    'dysthymia',
    'psychotic depression',
    'seasonal affective disorder',

    'bipolar I disorder',
    'bipolar II disorder',
    'bipolar disorder not otherwise specified',
    'cyclothymia',

    # Trauma and stressor related disorders
    'reactive attachment disorder',
    'disinhibited social engagement disorder',
    'post-traumatic stress disorder',
    'acute stress disorder',
    'adjustment disorder',
    'complex post-traumatic stress disorder',
    'prolonged grief disorder',

    # Neuro-developmental disorders
    'intellectual disability',
    'language disorder',
    'speech sound disorder',
    'social communication disorder',
    'attention deficit hyperactivity disorder',
    'developmental coordination disorder',
    'Tourette syndrome',
    'nonverbal learning Disorder (NVLD, NLD)',

    # Sleep-wake disorders
    'insomnia',
    'hypersomnia',
    'Kleine–Levin syndrome',
    'insufficient sleep syndrome',
    'narcolepsy',
    'restless legs syndrome',
    'sleep apnea',
    'night terrors',
    'exploding head syndrome',
    'sleep related movement disorder',

    'nightmare disorder',
    'rapid eye movement sleep behavior disorder',
    'confusional arousals',
    'sleepwalking',
    'sleep related eating disorder',
    'hypnagogic hallucinations',
    'hypnopompic hallucinations',

    'circadian rhythm sleep disorder',
    'delayed sleep phase disorder',
    'advanced sleep phase disorder',
    'irregular sleep–wake rhythm',
    'non-24-hour sleep–wake disorder',
    'jet lag',

    # Neuro-cognitive disorders
    'delirium',
    'dementia',
    'a traumatic brain injury',
    'amnesia',
    'chronic traumatic encephalopathy',
    'agnosia',

    # Substance-related and addictive disorders
    'alcoholism',
    'alcoholic hallucinosis',
    'alcohol withdrawal',

    'cannabis dependence',
    'cannabis intoxication',
    'cannabis withdrawal',
    'cannabis-induced delirium',
    'cannabis-induced psychosis',
    'cannabis-induced mood disorder',
    'cannabis-induced anxiety',

    'caffeine intoxication',
    'caffeine withdrawal',
    'caffeine-induced anxiety disorder',
    'caffeine-induced sleep disorder',

    'nicotine intoxication',
    'nicotine withdrawal',
    'nicotine dependence',

    'gambling disorder',
    'video game addiction',
    'Internet addiction disorder',
    'sexual addiction',
    'food addiction',
    'social media addiction',
    'pornography addiction',
    'shopping addiction',

    # Paraphilias
    'voyeuristic disorder',
    'exhibitionistic disorder',
    'frotteuristic disorder',
    'sexual masochism disorder',
    'sexual sadism disorder',

    # Somatic symptom related disorders
    'hypochondriasis',
    'Munchausen syndrome',

    # Disruptive impulse-control, and conduct disorders
    'oppositional defiant disorder',
    'intermittent explosive disorder',
    'antisocial personality disorder',
    'pyromania',
    'kleptomania',

    # Obsessive-compulsive and related disorders
    'obsessive–compulsive disorder',
    'compulsive hoarding',
    'olfactory reference syndrome',

    # Schizophrenia spectrum and other psychotic disorders
    'schizophrenia',
    'schizoaffective disorder',

    # Personality disorders
    'paranoid personality disorder',
    'schizoid personality disorder',
    'schizotypal personality disorder',

    'antisocial personality disorder',
    'borderline personality disorder',
    'histrionic personality disorder',
    'narcissistic personality disorder',

    'avoidant personality disorder',
    'dependent personality disorder',
    'obsessive–compulsive personality disorder',

    # Other
    'catatonia',
]

# the jokes are harder to come up with, but at the moment they look like a shoe
# so I might never edit this list again
GAG_CONDITIONS = [
    'being a vim user',
    'being an emacs user',
    'being an Xcode user',
    'being a VSCode user',
    'being a Notepad++ user',
    'running more than two Docker containers',
    'maintaining more than one browser profile',
    'using Windows Notepad as an IDE (???!)',
]

CONDITIONS = DSM_AND_ICD_CONDITIONS + GAG_CONDITIONS

del DSM_AND_ICD_CONDITIONS
del GAG_CONDITIONS

VERB_PHRASES = itertools.cycle([
    'I have diagnosed {patient} with',
    '{patient} appears to suffer from',
    'It seems that {patient}\'s life is made difficult by',
])
