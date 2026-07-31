---
layout: default
title: Nano Markup
description: A minimal, indentation-based data format for strings, mappings, and sequences.
permalink: /
---

<section class="hero">
  <p class="eyebrow">Nano Markup 1.0.0</p>
  <h1>Structured data,<br><span>without the visual noise.</span></h1>
  <p class="lede">Nano Markup is a minimal, indentation-based format for representing strings, mappings, and sequences in a form designed to be easy for people to read and write.</p>
  <div class="actions">
    <a class="button primary" href="https://nohainc.github.io/nanomarkup.github.com/specification.html">Read the specification</a>
    <a class="button" href="{{ '/implementations.html' | relative_url }}">Use Nano Markup</a>
  </div>
</section>

<section class="comparison" aria-labelledby="example-heading">
  <div class="section-heading">
    <p class="eyebrow">One value, two syntaxes</p>
    <h2 id="example-heading">Readable at a glance</h2>
  </div>
  <div class="code-grid">
    <figure>
      <figcaption>Nano Markup</figcaption>
      <pre><code>..
    name Ariana
    languages:
        Slovak
        English
    address|
        20 Forest Street
        811 01 Bratislava</code></pre>
    </figure>
    <figure>
      <figcaption>JSON</figcaption>
      <pre><code>{
  "name": "Ariana",
  "languages": [
    "Slovak",
    "English"
  ],
  "address": "20 Forest Street\n811 01 Bratislava"
}</code></pre>
    </figure>
  </div>
  <p class="example-link"><a href="https://github.com/nohainc/nanomarkup.spec/tree/v1.0.0/examples">Browse more paired Nano and JSON examples →</a></p>
</section>

<section class="model" aria-labelledby="model-heading">
  <div class="section-heading">
    <p class="eyebrow">The complete data model</p>
    <h2 id="model-heading">Exactly three value types</h2>
  </div>
  <div class="card-grid">
    <article>
      <span class="symbol">Aa</span>
      <h3>String</h3>
      <p>Unicode text, including empty and multiline text. Nano Markup does not infer numbers, booleans, nulls, or dates.</p>
    </article>
    <article>
      <span class="symbol">..</span>
      <h3>Mapping</h3>
      <p>An unordered association of unique string keys to values. Mappings may contain strings, mappings, and sequences.</p>
    </article>
    <article>
      <span class="symbol">:</span>
      <h3>Sequence</h3>
      <p>An ordered collection of values. Items may have different types, and duplicate items are preserved.</p>
    </article>
  </div>
</section>

<section class="syntax" aria-labelledby="syntax-heading">
  <div class="section-heading">
    <p class="eyebrow">Syntax at a glance</p>
    <h2 id="syntax-heading">A small language on purpose</h2>
  </div>
  <div class="syntax-table" role="table" aria-label="Nano Markup syntax summary">
    <div role="row"><span role="cell">Root mapping</span><code>..</code></div>
    <div role="row"><span role="cell">Root sequence</span><code>:</code></div>
    <div role="row"><span role="cell">String entry</span><code>name Ariana</code></div>
    <div role="row"><span role="cell">Nested mapping</span><code>contact..</code></div>
    <div role="row"><span role="cell">Nested sequence</span><code>languages:</code></div>
    <div role="row"><span role="cell">Multiline string</span><code>address|</code></div>
    <div role="row"><span role="cell">Comment</span><code># comment</code></div>
  </div>
  <p>Each structural level uses exactly four ASCII spaces. A document can also contain a string directly at its root. The conventional file extension is <code>.nano</code>.</p>
</section>

<section class="ecosystem" aria-labelledby="ecosystem-heading">
  <div class="section-heading">
    <p class="eyebrow">Start using it</p>
    <h2 id="ecosystem-heading">Specification and implementations</h2>
  </div>
  <div class="link-grid">
    <a href="https://github.com/nohainc/nanomarkup.spec/tree/v1.0.0">
      <strong>Language specification</strong>
      <span>Normative grammar, conformance fixtures, examples, and release history.</span>
    </a>
    <a href="https://github.com/nohainc/nanomarkup.python">
      <strong>Python implementation</strong>
      <small>Stable 1.0.0 · Python 3.11+</small>
      <span>Decode and encode Nano Markup using native Python values.</span>
    </a>
    <a href="https://github.com/nohainc/nanomarkup.go">
      <strong>Go implementation</strong>
      <small>Stable 1.0.0 · Go 1.24+</small>
      <span>Decode and encode with typed String, Mapping, and Sequence values.</span>
    </a>
    <a href="https://github.com/nohainc/nanomarkup.javascript">
      <strong>JavaScript &amp; TypeScript</strong>
      <small>Stable 1.0.0 · Node.js 22+ · Browsers</small>
      <span>Parse and stringify with ESM, CommonJS, and first-class types.</span>
    </a>
    <a href="https://github.com/nohainc/nanomarkup.dart">
      <strong>Dart implementation</strong>
      <small>Release ready · Dart 3.12+ · Web · Flutter</small>
      <span>Decode and encode using native Dart values across every Dart platform.</span>
    </a>
  </div>
  <p class="implementation-link"><a href="{{ '/implementations.html' | relative_url }}">Compare and install implementations →</a></p>
</section>

<section class="release-callout" aria-labelledby="release-heading">
  <div>
    <p class="eyebrow">Stable release</p>
    <h2 id="release-heading">Nano Markup 1.0.0</h2>
    <p>The first stable language specification was published on July 24, 2026. Stable releases are immutable; any known errors are recorded separately as errata.</p>
  </div>
  <a class="button" href="https://github.com/nohainc/nanomarkup.spec/releases/tag/v1.0.0">Release notes and downloads</a>
</section>

## About this repository

This repository contains the official Nano Markup website. The normative language specification and conformance suite are maintained in the [Nano Markup specification repository](https://github.com/nohainc/nanomarkup.spec). Website corrections and improvements are welcome through pull requests.
