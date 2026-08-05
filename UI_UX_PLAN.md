# Vibe Video — UI/UX Planning Document

**Version:** 2.0
**Date:** August 2026
**Status:** Planning Only — No Implementation
**Design Philosophy:** AI Creative Studio (Midjourney-inspired)

---

## Table of Contents

1. [Product Architecture](#1-product-architecture)
2. [User Experience (UX)](#2-user-experience-ux)
3. [User Interface (UI)](#3-user-interface-ui)
4. [System Design (Front-End)](#4-system-design-front-end)
5. [Core Screens](#5-core-screens)
6. [Video Generation Experience](#6-video-generation-experience)
7. [Chat Experience — Creative Workspace](#7-chat-experience--creative-workspace)
8. [Responsive Strategy](#8-responsive-strategy)
9. [Design System](#9-design-system)
10. [Final Notes](#10-final-notes)

---

## 1. Product Architecture

### 1.1 Application Overview

Vibe Video is a premium AI Creative Studio for generating motion-graphics videos from natural language. The interface is Midjourney-inspired: a professional creative workspace where users create, manage, iterate, and organize AI-generated videos. The generated video is always the hero — not the conversation.

**Tech Stack:** Tailwind CSS (CDN) + Vanilla JavaScript (ES6+) + Responsive (Desktop-first)

### 1.2 Page Structure

```
/ (Landing)                 — Marketing, featured videos, examples
/create                     — Three-panel creative workspace (PRIMARY)
/history                    — Visual gallery of all generations
/settings                   — Full settings page (advanced only)
```

### 1.3 Navigation Model

**Desktop — Three-panel workspace (/create):**
```
┌─────────────────────────────────────────────────────────────────────┐
│  [Logo]                        [Create]  [History]  [Settings]  [?]│
├────────────┬────────────────────────────────────┬──────────────────┤
│            │                                    │                  │
│  Left      │         Center Panel               │  Right Panel     │
│  Panel     │         (Main workspace)           │  (Settings)      │
│  (280px)   │                                    │  (300px)         │
│            │                                    │                  │
│  Conversa- │  ┌────────────────────────────┐   │  Generation      │
│  tions     │  │  Generated Video (Hero)    │   │  Settings        │
│  sidebar   │  │  [Large preview]           │   │                  │
│            │  │  [Actions: DL/Share/Edit]  │   │  Model selector  │
│  History   │  └────────────────────────────┘   │  Duration        │
│  Projects  │                                    │  Resolution      │
│  Search    │  ┌────────────────────────────┐   │  FPS             │
│            │  │  Conversation messages     │   │  Aspect ratio    │
│  [+ New]   │  │  AI responses              │   │  Style presets   │
│            │  │  Generation progress       │   │  Seed            │
│            │  └────────────────────────────┘   │  Advanced opts   │
│            │                                    │                  │
│            │  ┌────────────────────────────┐   │                  │
│            │  │  Prompt Dock (fixed)       │   │                  │
│            │  │  [Input] [Attach] [Gen ▶]  │   │                  │
│            │  └────────────────────────────┘   │                  │
├────────────┴────────────────────────────────────┴──────────────────┤
```

**Desktop — History (/history):**
```
┌─────────────────────────────────────────────────────────────────────┐
│  [Logo]                        [Create]  [History]  [Settings]  [?]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Your Creations                          [Search: _________] [Grid] │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │  ▶       │ │  ▶       │ │  ▶       │ │  ▶       │             │
│  │  Thumb   │ │  Thumb   │ │  Thumb   │ │  Thumb   │             │
│  │          │ │          │ │          │ │          │             │
│  │ Duration │ │ Duration │ │ Duration │ │ Duration │             │
│  │ Prompt   │ │ Prompt   │ │ Prompt   │ │ Prompt   │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │  ▶       │ │  ▶       │ │  ▶       │ │  ▶       │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.4 User Flow Summary

```
Landing → "Create Studio" → /create workspace
                                    ↓
                    Left panel: New conversation
                                    ↓
                    Center: Prompt dock → Type prompt
                                    ↓
                    Right panel: Adjust settings
                                    ↓
                    Center: AI responds, confirms brief
                                    ↓
                    Center: Generation pipeline visualizes stages
                                    ↓
                    Center: Video appears as HERO (large preview)
                                    ↓
                    Actions: Download / Share / Edit / Regenerate
                                    ↓
                    Left panel: Conversation saved to history
```

---

## 2. User Experience (UX)

### 2.1 Design Philosophy

The application should **never** feel like ChatGPT with video generation. Instead, it should feel like a **professional creative workspace** — a world-class AI Creative Studio designed specifically for professional video generation.

**Core principles:**
- Generated video is always the visual focal point
- Conversation becomes secondary after generation
- Professional editor feel, not chatbot feel
- Premium dark theme with minimal distractions
- Spacious layouts with strong visual hierarchy
- Elegant micro-interactions that enhance workflow

### 2.2 First-Time Visitor Journey

| Step | Screen | Action |
|------|--------|--------|
| 1 | Landing | See hero, featured videos, trending creations |
| 2 | Click "Create Studio" | Enter three-panel workspace |
| 3 | Left panel | Click "New Conversation" |
| 4 | Center panel | See prompt dock with categorized suggestions |
| 5 | Right panel | Adjust default settings |
| 6 | Type prompt | Use prompt dock input |
| 7 | AI responds | Confirms video brief in center panel |
| 8 | User confirms | Clicks "Generate" in prompt dock |
| 9 | Center panel | Generation pipeline visualizes 7 stages |
| 10 | Center panel | Video appears as HERO — large preview |
| 11 | Post-gen | Download, share, edit, or regenerate |
| 12 | Left panel | Conversation auto-saved to history |

### 2.3 Returning User Journey

| Step | Screen | Action |
|------|--------|--------|
| 1 | Landing | Click "Create" or see recent in /history |
| 2 | Left panel | See conversation history, pinned favorites |
| 3 | Select conversation | Resume previous session |
| 4 | Center panel | Continue iterating on video |
| 5 | Right panel | Adjust settings for next generation |

### 2.4 Empty States

**/create — No conversations:**
```
┌─────────────────────────────────────────────────────────────┐
│  Left Panel (280px)                                         │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🔍 Search conversations...                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  + New Conversation                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ─── Today ──────────────────────────────────────────────  │
│                                                             │
│  (empty — no conversations yet)                             │
│                                                             │
│  ─── Pinned ─────────────────────────────────────────────  │
│                                                             │
│  (empty — pin favorite conversations here)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**/history — No generations:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              No videos yet                                  │
│                                                             │
│   Your generated videos will appear here.                   │
│   Start creating to build your collection.                  │
│                                                             │
│   [Create Your First Video →]                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.5 Loading States

**Video generation in progress:**
- Center panel shows generation pipeline (7 stages)
- Each stage has clear visual status indicator
- Prompt dock shows "Generating..." with progress

**Page loading:**
- Skeleton screens for gallery items
- Shimmer animation on video cards
- No spinners — prefer content placeholders

### 2.6 Error States

**Generation failed (center panel):**
```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️  Generation Failed                                      │
│                                                             │
│  The video could not be generated.                          │
│  Reason: [error message from API]                           │
│                                                             │
│  [Try Again]  [Edit Prompt]  [Report Issue]                 │
└─────────────────────────────────────────────────────────────┘
```

**Network error:**
- Toast notification: "Connection lost. Retrying..."
- Auto-retry with exponential backoff
- Manual "Retry" button after 3 failures

**API key missing:**
```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️  Backend Not Connected                                  │
│                                                             │
│  Connect to your Vibe Video backend to start creating.      │
│                                                             │
│  Backend URL: [https://abundant-analysis-...]               │
│  [Test Connection]  [Connect →]                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.7 Success States

**Video generation complete:**
- Video appears as HERO in center panel (large preview)
- Success toast: "Video generated successfully!"
- Download and share buttons prominent
- Conversation saved to left panel history
- Option to "Regenerate" or "Iterate" in prompt dock

### 2.8 Accessibility

- Keyboard navigation for all elements
- ARIA labels on buttons/inputs/video players
- WCAG AA contrast (4.5:1 text, 3:1 large text)
- Respect `prefers-reduced-motion`
- Focus visible rings on all interactive elements
- Alt text on all video thumbnails
- Skip to main content link
- Screen reader support for generation pipeline stages

### 2.9 Performance UX

- Lazy load gallery below fold
- Skeleton screens (not spinners)
- Optimistic updates (show state immediately)
- Debounced input
- Cached responses in localStorage
- Progressive loading (preview first, full quality on demand)

---

## 3. User Interface (UI)

### 3.1 Visual Hierarchy

```
Primary:    Generated video preview (HERO — center panel, large)
Secondary:  Prompt dock (fixed bottom, always visible)
Tertiary:   Right panel settings (persistent sidebar)
Quaternary: Left panel conversations (narrow sidebar)
Quinary:    Meta info (timestamps, durations, tokens)
```

**Key principle:** The generated video is always the visual focal point. After generation, the conversation becomes secondary.

### 3.2 Layout — Three-Panel Workspace (/create)

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Logo]  [Vibe Video]     [Create]  [History]  [Settings]  [?]    │
├────────────┬────────────────────────────────────┬──────────────────┤
│            │                                    │                  │
│  LEFT      │         CENTER PANEL               │  RIGHT PANEL     │
│  PANEL     │         (Main workspace)           │  (Settings)      │
│  (280px)   │         (flex: 1)                  │  (300px)         │
│            │                                    │                  │
│  ┌───────┐ │  ┌────────────────────────────┐   │  Generation      │
│  │Search │ │  │                            │   │  Settings        │
│  └───────┘ │  │   VIDEO PREVIEW (HERO)     │   │                  │
│            │  │   (16:9, large)             │   │  Model: [▼]     │
│  [+New]    │  │                            │   │  Duration: [▼]   │
│            │  │   [▶ Play] [DL] [Share]    │   │  Resolution: [▼] │
│  Today     │  │   [Edit] [Regen] [More]    │   │  FPS: [▼]       │
│  ─────     │  │                            │   │  Ratio: [▼]      │
│  Conv 1    │  └────────────────────────────┘   │                  │
│  Conv 2    │                                    │  Style Presets   │
│  Conv 3    │  ┌────────────────────────────┐   │  ──────────────  │
│            │  │  AI: Here's your video!     │   │  [Cinematic]     │
│  Yesterday │  │  The animation shows...     │   │  [Anime]         │
│  ─────     │  │                            │   │  [Documentary]   │
│  Conv 4    │  │  User: Make it slower      │   │  [Nature]        │
│            │  │                            │   │  [Product Ads]   │
│  Older     │  │  AI: I'll regenerate...    │   │  [Motion Graphics]│
│  ─────     │  │                            │   │                  │
│  Conv 5    │  │  Generating...              │   │  Advanced Options│
│  Conv 6    │  │  [Pipeline visualization]  │   │  ──────────────  │
│            │  │                            │   │  Seed: [____]    │
│  ──────    │  └────────────────────────────┘   │  [x] Strict mode │
│  Pinned    │                                    │                  │
│  ─────     │  ┌────────────────────────────┐   │                  │
│  Star 1    │  │  PROMPT DOCK (fixed)       │   │                  │
│  Star 2    │  │  ┌──────────────────────┐  │   │                  │
│            │  │  │ Type your prompt...   │  │   │                  │
│            │  │  │ [Paperclip] [Film] [Reference] │  │   │               │
│            │  │  └──────────────────────┘  │   │                  │
│            │  │  [Dur: 30s] [Ratio: 16:9] │   │                  │
│            │  │  [Model: Vibe] [Generate ▶]│   │                  │
│            │  └────────────────────────────┘   │                  │
├────────────┴────────────────────────────────────┴──────────────────┤
```

### 3.3 Typography

**Primary font:** Inter (Google Fonts)
**Monospace font:** JetBrains Mono (for code/technical prompts)

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| H1 (hero) | 48-64px | 700 | #fafafa |
| H2 (section) | 28-36px | 600 | #fafafa |
| H3 (card title) | 20-24px | 600 | #fafafa |
| Body | 16px | 400 | #a1a1aa (zinc-400) |
| Small / meta | 12-14px | 400 | #71717a (zinc-500) |
| Code / prompts | 14px | 400 | #d4d4d8 (zinc-300) |
| Button | 14-16px | 500 | #fafafa |
| Input placeholder | 16px | 400 | #52525b (zinc-600) |

### 3.4 Spacing System

Base unit: **4px**

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Icon gaps, tight padding |
| sm | 8px | Button padding, small gaps |
| md | 12px | Card internal padding |
| lg | 16px | Input padding, section gaps |
| xl | 24px | Card padding, content gaps |
| 2xl | 32px | Section margins |
| 3xl | 48px | Page margins |
| 4xl | 64px | Hero spacing |
| 5xl | 96px | Major section breaks |

### 3.5 Colors

**Dark theme palette:**

| Token | Hex | Usage |
|-------|-----|-------|
| bg-primary | #09090b (zinc-950) | Page background |
| bg-secondary | #18181b (zinc-900) | Cards, panels |
| bg-tertiary | #27272a (zinc-800) | Hover states, elevated surfaces |
| bg-accent | #3f3f46 (zinc-700) | Active states |
| border-default | rgba(255,255,255,0.06) | Subtle card borders |
| border-hover | rgba(255,255,255,0.1) | Hover borders |
| border-active | rgba(139,92,246,0.3) | Active/selected borders |
| text-primary | #fafafa (zinc-50) | Headings, primary text |
| text-secondary | #a1a1aa (zinc-400) | Body text |
| text-tertiary | #71717a (zinc-500) | Meta, timestamps |
| accent | #8b5cf6 (violet-500) | Primary CTA, links |
| accent-hover | #7c3aed (violet-600) | CTA hover |
| accent-glow | rgba(139,92,246,0.15) | Glow effects |
| success | #22c55e (green-500) | Success states |
| error | #ef4444 (red-500) | Error states |
| warning | #f59e0b (amber-500) | Warning states |

### 3.6 Components

**Card (Video Card):**
- Background: bg-secondary
- Border: 1px solid border-default
- Border radius: 12px
- Padding: 16px
- Hover: border-hover, subtle lift (translateY(-2px))
- Video thumbnail: 16:9 aspect ratio, overflow hidden

**Button — Primary:**
- Background: accent (violet-500)
- Text: white
- Padding: 12px 24px
- Border radius: 8px
- Font: 14px, weight 500
- Hover: accent-hover (violet-600)
- Transition: 150ms ease

**Button — Secondary:**
- Background: transparent
- Border: 1px solid border-default
- Text: text-primary
- Padding: 12px 24px
- Border radius: 8px
- Hover: bg-tertiary

**Button — Ghost:**
- Background: transparent
- Text: text-secondary
- Padding: 8px 16px
- Hover: bg-tertiary
- No border

**Input (Prompt Dock):**
- Background: bg-secondary
- Border: 1px solid border-default
- Border radius: 12px
- Padding: 16px
- Font: 16px
- Focus: accent border, accent-glow shadow
- Placeholder: text-tertiary

**Chat Message — AI:**
- Background: bg-secondary
- Border: 1px solid border-default
- Border radius: 12px (top-left: 4px)
- Padding: 16px
- Max-width: 80%

**Chat Message — User:**
- Background: accent (violet-500)
- Text: white
- Border radius: 12px (top-right: 4px)
- Padding: 16px
- Max-width: 80%
- Margin-left: auto

**Video Preview Card (HERO):**
- Background: bg-primary
- Border: 1px solid border-default
- Border radius: 12px
- Overflow: hidden
- Video: 16:9 aspect ratio
- Overlay: play button on hover
- Actions row below video

**Conversation Item (Left Panel):**
- Background: transparent
- Border-radius: 8px
- Padding: 12px 16px
- Hover: bg-tertiary
- Active: bg-accent + border-active
- Pinned: star icon + accent color

**Generation Pipeline Stage:**
- Background: bg-secondary
- Border: 1px solid border-default
- Border radius: 8px
- Status indicator: colored dot (pending/active/complete/error)

### 3.7 Icons

**Icon library:** Lucide Icons (via CDN — single SVG sprite)

| Icon | Usage |
|------|-------|
| play / pause | Video controls |
| download | Download video |
| share-2 | Share action |
| refresh-cw | Regenerate |
| settings | Settings page |
| history | History page |
| plus-circle | New conversation |
| trash-2 | Delete |
| copy | Copy prompt |
| check | Success state |
| alert-circle | Error state |
| loader | Loading state |
| send | Send message |
| menu | Mobile menu |
| x | Close / dismiss |
| chevron-down | Dropdown |
| search | Search history |
| pin | Pin conversation |
| star | Favorite |
| archive | Archive conversation |
| image | Attach image |
| film | Attach video |
| link | Attach reference |
| sliders | Settings panel |
| Sparkles | AI generation |

### 3.8 Animations & Micro-Interactions

**Global rules:**
- Duration: 150-300ms
- Easing: cubic-bezier(0.4, 0, 0.2, 1) (ease-out)
- Respect `prefers-reduced-motion`

**Specific animations:**

| Element | Animation | Duration |
|---------|-----------|----------|
| Button hover | Scale(1.02) + shadow | 150ms |
| Card hover | translateY(-2px) + border glow | 200ms |
| Page transition | Fade in + slide up 8px | 300ms |
| Toast notification | Slide in from top-right | 300ms |
| Video preview | Fade in + scale(0.98→1) | 300ms |
| Chat message | Fade in + slide up 4px | 200ms |
| Loading dots | Pulsing opacity | 1s loop |
| Progress bar | Width transition | 500ms |
| Success checkmark | Draw stroke | 600ms |
| Panel resize | Width transition | 200ms |
| Pipeline stage | Fade in + slide right | 200ms |

**Glassmorphism effect (subtle):**
```css
/* Card glassmorphism */
background: rgba(24, 24, 27, 0.8);
backdrop-filter: blur(12px);
border: 1px solid rgba(255, 255, 255, 0.06);
```

Used on:
- Floating action buttons
- Modal overlays
- Settings drawer
- Prompt dock

---

## 4. System Design (Front-End)

### 4.1 Component Hierarchy

```
App
├── Layout
│   ├── TopBar
│   │   ├── Logo
│   │   ├── NavLinks (Create, History, Settings)
│   │   ├── MobileMenuButton
│   │   └── ThemeToggle
│   ├── LeftPanel (280px, collapsible)
│   │   ├── SearchBar
│   │   ├── NewConversationButton
│   │   ├── ConversationList
│   │   │   ├── ConversationGroup (Today)
│   │   │   │   └── ConversationItem (×n)
│   │   │   ├── ConversationGroup (Yesterday)
│   │   │   │   └── ConversationItem (×n)
│   │   │   ├── ConversationGroup (Older)
│   │   │   │   └── ConversationItem (×n)
│   │   │   └── PinnedGroup
│   │   │       └── ConversationItem (×n)
│   │   └── ConversationActions (rename, duplicate, archive, delete, pin)
│   ├── CenterPanel (flex: 1)
│   │   ├── VideoHero
│   │   │   ├── VideoPlayer (16:9, large)
│   │   │   ├── VideoActions (download, share, edit, regenerate)
│   │   │   └── VideoMetadata (prompt, duration, model, etc.)
│   │   ├── MessageList
│   │   │   ├── AIMessage
│   │   │   │   ├── TextContent
│   │   │   │   ├── VideoPreview
│   │   │   │   └── SuggestionChips
│   │   │   └── UserMessage
│   │   │       └── TextContent
│   │   ├── GenerationPipeline
│   │   │   └── PipelineStage (×7)
│   │   │       ├── StageIcon
│   │   │       ├── StageLabel
│   │   │       └── StageStatus (pending/active/complete/error)
│   │   └── PromptDock (fixed bottom)
│   │       ├── TextArea (auto-expanding)
│   │       ├── AttachmentButtons (image, video, reference)
│   │       ├── QuickSettings (duration, ratio, model)
│   │       └── GenerateButton
│   └── RightPanel (300px, collapsible)
│       ├── GenerationSettings
│       │   ├── ModelSelector
│       │   ├── DurationSelector
│       │   ├── ResolutionSelector
│       │   ├── FPSSelector
│       │   └── AspectRatioSelector
│       ├── StylePresets
│       │   └── PresetChip (×n)
│       └── AdvancedOptions
│           ├── SeedInput
│           └── StrictModeToggle
├── Pages
│   ├── LandingPage
│   │   ├── HeroSection
│   │   ├── FeaturedVideos
│   │   ├── TrendingCreations
│   │   ├── ExamplePrompts (categorized)
│   │   ├── HowItWorks
│   │   ├── FeatureOverview
│   │   └── CTASection
│   ├── CreatePage
│   │   └── ThreePanelWorkspace (see above)
│   ├── HistoryPage
│   │   ├── SearchBar
│   │   ├── FilterTabs
│   │   ├── SortOptions
│   │   └── VideoGallery (masonry/grid)
│   │       └── RichVideoCard (×n)
│   │           ├── Thumbnail
│   │           ├── PlayButton
│   │           ├── Duration
│   │           ├── Resolution
│   │           ├── FPS
│   │           ├── Model
│   │           ├── CreationDate
│   │           ├── GenerationTime
│   │           ├── PromptPreview
│   │           ├── FileSize
│   │           └── Actions (play, download, share, duplicate, edit, regen, delete)
│   └── SettingsPage
│       ├── APIConfiguration
│       ├── DefaultGenerationSettings
│       ├── AppearanceSettings
│       └── AboutSection
├── Shared
│   ├── Toast
│   ├── Modal
│   ├── Drawer (slide-out settings)
│   ├── Skeleton
│   ├── Spinner
│   ├── EmptyState
│   ├── ErrorState
│   ├── Tooltip
│   ├── Dropdown
│   ├── Tabs
│   └── Badge
└── Utils
    ├── dom.js
    ├── format.js
    ├── storage.js
    └── api.js
```

### 4.2 Reusable UI Components

| Component | Props | Description |
|-----------|-------|-------------|
| `Button` | variant, size, icon, loading, disabled | Primary/secondary/ghost button |
| `Card` | padding, hover, glass | Content container |
| `VideoCard` | thumbnail, duration, prompt, actions | Rich video card |
| `Input` | type, placeholder, value, onChange | Text input |
| `TextArea` | rows, placeholder, autoResize | Multi-line input |
| `Badge` | variant, text | Status labels |
| `Avatar` | src, size, fallback | User/system avatar |
| `Toast` | type, message, duration | Notification popup |
| `Modal` | isOpen, onClose, title | Overlay dialog |
| `Drawer` | isOpen, onClose, side, width | Slide-out panel |
| `Skeleton` | width, height, variant | Loading placeholder |
| `Spinner` | size | Loading indicator |
| `EmptyState` | icon, title, description, action | No-data display |
| `ErrorState` | icon, title, description, action | Error display |
| `VideoPlayer` | src, poster, controls | Video playback |
| `Tooltip` | content, position | Hover tooltip |
| `Dropdown` | options, value, onChange | Select menu |
| `Tabs` | tabs, activeTab, onChange | Tab navigation |
| `SearchBar` | value, onChange, placeholder | Search input |
| `ConversationItem` | title, timestamp, pinned, active | Conversation list item |
| `PipelineStage` | label, status, icon | Generation pipeline stage |
| `PromptDock` | onGenerate, settings | Fixed prompt input area |
| `StylePreset` | name, selected, onClick | Style preset chip |

### 4.3 Folder Structure

```
frontend/
├── index.html                    # Landing page
├── create.html                   # Three-panel creative workspace
├── history.html                  # Visual gallery page
├── settings.html                 # Full settings page
├── css/
│   ├── globals.css               # Reset, base styles, CSS variables
│   ├── components.css            # Reusable component styles
│   ├── layout.css                # Three-panel layout styles
│   └── animations.css            # Keyframes, transitions
├── js/
│   ├── app.js                    # Main app init, routing
│   ├── store.js                  # State management
│   ├── api.js                    # API client (fetch wrapper)
│   ├── components/
│   │   ├── Button.js
│   │   ├── Card.js
│   │   ├── VideoCard.js
│   │   ├── Input.js
│   │   ├── Toast.js
│   │   ├── Modal.js
│   │   ├── Drawer.js
│   │   ├── Skeleton.js
│   │   ├── VideoPlayer.js
│   │   ├── ChatMessage.js
│   │   ├── PromptDock.js
│   │   ├── ConversationItem.js
│   │   ├── PipelineStage.js
│   │   ├── StylePreset.js
│   │   └── SearchBar.js
│   ├── pages/
│   │   ├── landing.js
│   │   ├── create.js
│   │   ├── history.js
│   │   └── settings.js
│   └── utils/
│       ├── dom.js                # DOM helpers
│       ├── format.js             # Date/number formatting
│       └── storage.js            # localStorage wrapper
├── assets/
│   ├── icons/                    # SVG icons (inline)
│   └── fonts/                    # Self-hosted fonts (optional)
└── favicon.ico
```

### 4.4 Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| CSS classes | kebab-case | `.video-card`, `.prompt-dock` |
| CSS variables | kebab-case with `--` | `--color-bg-primary` |
| JS functions | camelCase | `sendMessage()`, `generateVideo()` |
| JS classes | PascalCase | `ChatMessage`, `VideoPlayer` |
| JS constants | UPPER_SNAKE_CASE | `API_BASE_URL`, `MAX_RETRIES` |
| HTML IDs | kebab-case | `chat-area`, `prompt-dock` |
| HTML data-* | kebab-case | `data-video-id`, `data-state` |
| Files | kebab-case | `video-player.js`, `chat-message.js` |

### 4.5 State Management

**Approach:** Vanilla JS with a simple state store pattern

```javascript
const state = {
  // Current page
  currentPage: 'create',

  // Left panel - conversations
  conversations: [],
  activeConversationId: null,
  conversationSearch: '',

  // Center panel - chat/video
  messages: [],
  lastGeneratedVideo: null,
  isGenerating: false,
  generationProgress: { stage: 0, stages: [] },

  // Right panel - settings
  settings: {
    model: 'vibe-video',
    duration: 30,
    resolution: '1080p',
    fps: 30,
    aspectRatio: '16:9',
    stylePreset: null,
    seed: null,
    strictMode: false,
  },

  // History
  videos: [],
  historySearch: '',
  historyFilter: 'all',
  historySort: 'newest',

  // UI state
  leftPanelOpen: true,
  rightPanelOpen: true,
  activeModal: null,
  activeDrawer: null,
  toasts: [],
};
```

**Persistence:**
- Settings → `localStorage`
- Video history → `localStorage` (metadata only)
- Conversations → `localStorage`
- Current session → `sessionStorage`

---

## 5. Core Screens

### 5.1 Landing Page

**Purpose:** First impression, demonstrate creative capabilities.

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Logo]  [Vibe Video]              [Create Free Video →]           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                    ✨ Create AI Videos                              │
│               with Natural Language                                 │
│                                                                     │
│       Describe what you want. Vibe Video brings it                  │
│       to life as stunning motion graphics.                          │
│                                                                     │
│                  [Start Creating →]                                 │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Featured Videos                                                    │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │  ▶       │ │  ▶       │ │  ▶       │ │  ▶       │             │
│  │  Video 1 │ │  Video 2 │ │  Video 3 │ │  Video 4 │             │
│  │  30s     │ │  15s     │ │  45s     │ │  20s     │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Trending Creations                                                 │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │  ▶       │ │  ▶       │ │  ▶       │ │  ▶       │             │
│  │  Video 5 │ │  Video 6 │ │  Video 7 │ │  Video 8 │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Example Prompts (Categorized)                                      │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  [Cinematic] [Anime] [Documentary] [Nature] [Product Ads]          │
│  [Storytelling] [Architecture] [Education] [Motion Graphics]       │
│  [Logo Reveal] [Social Media]                                       │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  🎬 "Create a cinematic drone shot over a futuristic       │   │
│  │      city at sunset with neon lights reflecting on water"   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  How It Works                                                       │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  [1. Describe] → [2. Generate] → [3. Download]                     │
│                                                                     │
│  1. Describe your video in natural language                         │
│  2. AI generates your video in seconds                              │
│  3. Download, share, or iterate                                     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Features                                                           │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  [🎬 AI Generation] [🎨 Style Presets] [⚡ Fast Rendering]         │
│  [📱 Responsive] [🔒 Private] [🔄 Iteration]                       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  [Footer: GitHub | Docs | API | Privacy]                            │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 History Page — Visual Gallery

**Purpose:** Browse, search, and manage past generations.

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Logo]              [Create] [History] [Settings]                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Your Creations                                                     │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  [🔍 Search: _______________]  [All] [Recent] [Starred]  [↕] │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Masonry Grid:                                                      │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │  ▶       │ │  ▶       │ │  ▶       │ │  ▶       │             │
│  │  Thumb   │ │  Thumb   │ │  Thumb   │ │  Thumb   │             │
│  │          │ │          │ │          │ │          │             │
│  │ 30s HD   │ │ 15s 4K   │ │ 45s HD   │ │ 20s SD   │             │
│  │ 2m ago   │ │ 1h ago   │ │ 1d ago   │ │ 3d ago   │             │
│  │ Prompt.. │ │ Prompt.. │ │ Prompt.. │ │ Prompt.. │             │
│  │ [DL][⋯]  │ │ [DL][⋯]  │ │ [DL][⋯]  │ │ [DL][⋯]  │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │  ▶       │ │  ▶       │ │  ▶       │ │  ▶       │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Features:**
- Masonry/grid layout toggle
- Search bar (searches prompt text)
- Filter tabs: All | Recent | Starred
- Sort dropdown: Newest | Oldest | Most viewed
- Hover preview (quick play on hover)
- Quick actions on hover (download, share, delete)
- Rich video cards with metadata

### 5.3 Settings Page

**Purpose:** Full settings for advanced preferences.

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Logo]              [Create] [History] [Settings]                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Settings                                                           │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  API Configuration                                            │  │
│  │  ─────────────────────────────────────────────────────────── │  │
│  │                                                               │  │
│  │  Backend URL                                                  │  │
│  │  ┌──────────────────────────────────────────────────────┐    │  │
│  │  │ https://abundant-analysis-...up.railway.app          │    │  │
│  │  └──────────────────────────────────────────────────────┘    │  │
│  │                                                               │  │
│  │  [Test Connection]  [Connected ✓]                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Default Generation Settings                                  │  │
│  │  ─────────────────────────────────────────────────────────── │  │
│  │                                                               │  │
│  │  Model:      [Vibe Video (Hyperframes) ▼]                    │  │
│  │  Duration:   [30s ▼]                                          │  │
│  │  Resolution: [1080p ▼]                                        │  │
│  │  FPS:        [30 ▼]                                           │  │
│  │  Ratio:      [16:9 ▼]                                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Appearance                                                   │  │
│  │  ─────────────────────────────────────────────────────────── │  │
│  │                                                               │  │
│  │  Theme:       [Dark ▼]                                        │  │
│  │  Accent:      [Violet ▼]                                      │  │
│  │  Sidebar:     [Expanded by default ✓]                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  About                                                        │  │
│  │  ─────────────────────────────────────────────────────────── │  │
│  │  Version: 2.0.0                                               │  │
│  │  GitHub: [link]                                               │  │
│  │  API Docs: [link]                                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.4 Error Page (404)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                         404                                         │
│                    Page not found                                    │
│                                                                     │
│          The page you're looking for doesn't exist.                  │
│                                                                     │
│                    [Go Home →]                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. Video Generation Experience

### 6.1 Prompt Dock (Fixed Bottom)

**The primary input element — always visible, never scrolls away.**

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ✨ Describe the video you want to create...                  │  │
│  │                                                               │  │
│  │  (auto-expanding textarea, min 3 lines, max 8)               │  │
│  │                                                               │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │  📷 Attach image  |  🎬 Attach video  |  🔗 Reference  │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  [Duration: 30s ▼] [Ratio: 16:9 ▼] [Model: Vibe ▼] [Generate ▶]│
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Features:**
- Auto-expanding textarea (min 80px, max 240px height)
- Character count (subtle, bottom-right)
- Keyboard shortcut: Cmd/Ctrl + Enter to send
- Attachment buttons: image, video, reference
- Quick settings row: duration, ratio, model
- Large, prominent Generate button
- Fixed at bottom, always visible while scrolling

### 6.2 Generation Pipeline Visualization

**Instead of only a progress bar, visualize the AI workflow.**

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  🎬 Generating your video...                                        │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │  ● Understanding Prompt                                       │  │
│  │  │   ✅ Complete (2s)                                          │  │
│  │  │                                                            │  │
│  │  ● Planning Scenes                                            │  │
│  │  │   ✅ Complete (5s)                                          │  │
│  │  │                                                            │  │
│  │  ● Storyboarding                                              │  │
│  │  │   ✅ Complete (3s)                                          │  │
│  │  │                                                            │  │
│  │  ● Generating Frames                                          │  │
│  │  │   🔄 In progress... (12s)                                  │  │
│  │  │                                                            │  │
│  │  ○ Rendering                                                  │  │
│  │  │   ⏳ Waiting                                               │  │
│  │  │                                                            │  │
│  │  ○ Encoding                                                   │  │
│  │  │   ⏳ Waiting                                               │  │
│  │  │                                                            │  │
│  │  ○ Finalizing                                                 │  │
│  │      ⏳ Waiting                                               │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Estimated: ~2 minutes remaining                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Pipeline stages:**

| Stage | Description | Icon |
|-------|-------------|------|
| 1. Understanding Prompt | AI analyzes the prompt | Brain |
| 2. Planning Scenes | AI plans the video structure | Layout |
| 3. Storyboarding | AI creates scene breakdown | BookOpen |
| 4. Generating Frames | AI generates visual content | Image |
| 5. Rendering | Hyperframes renders HTML to frames | Monitor |
| 6. Encoding | FFmpeg encodes to MP4 | Film |
| 7. Finalizing | Final processing and delivery | CheckCircle |

### 6.3 Generated Video Preview (HERO)

**Whenever a generation finishes, the video becomes the visual focal point.**

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ✅ Here's your video!                                              │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                                                               │  │
│  │              VIDEO PREVIEW (HERO)                             │  │
│  │              (16:9, large, 600px+ height)                     │  │
│  │                                                               │  │
│  │                    [▶ Play]                                    │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                       │
│  │ ⬇  │ │ 🔗 │ │ 📝 │ │ 🔄 │ │ ⋯  │ │ 🗑 │                       │
│  │Down│ │Share│ │Edit│ │Retry│ │More│ │Del │                       │
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘                       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Prompt: "Animate Dijkstra's algorithm on a 5-node graph"    │  │
│  │  Duration: 30s | Quality: Standard | FPS: 30 | Model: Vibe   │  │
│  │  Generated: 2 minutes ago | Size: 2.4 MB                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.4 Rich Video Card (History Gallery)

```
┌──────────────────────────────────┐
│  ┌──────────────────────────┐   │
│  │  VIDEO THUMBNAIL         │   │
│  │  (16:9, hover to play)   │   │
│  │                          │   │
│  │       [▶]                │   │
│  │                          │   │
│  │  30s  |  1080p  |  30fps │   │
│  └──────────────────────────┘   │
│                                   │
│  Prompt: "Animate Dijkstra's..." │
│                                   │
│  Model: Vibe | 2m ago | 2.4 MB  │
│                                   │
│  [⬇] [🔗] [🔄] [⋯]            │
└──────────────────────────────────┘
```

**Metadata displayed:**
- Thumbnail (16:9)
- Duration
- Resolution
- FPS
- Model
- Creation date
- Generation time
- Prompt preview (truncated)
- File size

**Actions:**
- Play (thumbnail click)
- Download
- Share
- Duplicate
- Edit Prompt
- Regenerate
- Delete (with confirmation)

### 6.5 Download Actions

| Action | Button | Behavior |
|--------|--------|----------|
| Download MP4 | ⬇ Download | Direct download of .mp4 file |
| Copy prompt | 📝 Copy | Copies original prompt to clipboard |
| View details | ⋯ More | Shows generation metadata |

### 6.6 Share Actions

| Action | Button | Behavior |
|--------|--------|----------|
| Copy link | 🔗 Share | Copies video URL to clipboard |
| Embed code | < /> Embed | Copies HTML embed snippet |

### 6.7 Regenerate Flow

**Option 1: Same prompt, retry**
- Click "Regenerate" button
- Uses same prompt and settings
- Creates new generation

**Option 2: Edit prompt, iterate**
- Click "Edit Prompt" button
- Prompt appears in prompt dock
- User modifies and regenerates

**Option 3: Full redo**
- Click "New Video" in context menu
- Clears center panel, starts fresh

---

## 7. Chat Experience — Creative Workspace

### 7.1 Center Panel Layout

**The center panel is the primary workspace — where all creative work happens.**

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CENTER PANEL                                                       │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  VIDEO PREVIEW (HERO) — when video is ready                   │  │
│  │  (large, prominent, 16:9 aspect ratio)                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  CONVERSATION MESSAGES                                        │  │
│  │  (scrollable, secondary to video)                             │  │
│  │                                                               │  │
│  │  AI: Here's your video! The animation shows...                │  │
│  │                                                               │  │
│  │  User: Make it slower in scene 2                              │  │
│  │                                                               │  │
│  │  AI: I'll regenerate with slower pacing...                    │  │
│  │                                                               │  │
│  │  🎬 GENERATION PIPELINE                                       │  │
│  │  (when generating)                                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  PROMPT DOCK (fixed bottom)                                   │  │
│  │  [Input] [Attach] [Settings] [Generate]                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 Message Types

1. **Text only** — Simple explanation or question
2. **Text + suggestions** — Response with clickable suggestion chips
3. **Text + video** — Response with embedded video preview (HERO)
4. **Text + progress** — Response with generation pipeline
5. **Error** — Error message with retry option

### 7.3 Prompt Suggestions (Categorized)

**Replace simple placeholder prompts with categorized inspiration.**

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ✨ What would you like to create?                                  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  🎬 Cinematic                                                │  │
│  │  • "Create a cinematic drone shot over a futuristic city"    │  │
│  │  • "Film noir scene with rain and neon signs"                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  🎨 Anime                                                    │  │
│  │  • "Anime-style character transformation sequence"           │  │
│  │  • "Studio Ghibli landscape with floating islands"           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  📽️ Documentary                                               │  │
│  │  • "Explain quantum entanglement with visual metaphors"      │  │
│  │  • "History of the internet in 30 seconds"                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  🌿 Nature                                                    │  │
│  │  • "Timelapse of a flower blooming in 4K"                    │  │
│  │  • "Ocean waves crashing on volcanic rocks"                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  [Product Ads] [Storytelling] [Architecture] [Education]           │
│  [Motion Graphics] [Logo Reveal] [Social Media]                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Categories:**
- Cinematic
- Anime
- Documentary
- Nature
- Product Ads
- Storytelling
- Architecture
- Education
- Motion Graphics
- Logo Reveal
- Social Media

### 7.4 Conversation History (Left Panel)

**Full conversation manager with search, grouping, and actions.**

```
┌─────────────────────────────────────────────────────────────────────┐
│  LEFT PANEL (280px)                                                 │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  🔍 Search conversations...                                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  + New Conversation                                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ─── Pinned ─────────────────────────────────────────────────────  │
│                                                                     │
│  ⭐ Dijkstra Animation                                              │
│     2 hours ago                                                     │
│                                                                     │
│  ⭐ Fourier Series                                                  │
│     Yesterday                                                       │
│                                                                     │
│  ─── Today ──────────────────────────────────────────────────────  │
│                                                                     │
│  Quantum Entanglement                                               │
│     10 minutes ago                                                  │
│                                                                     │
│  Gradient Descent                                                   │
│     1 hour ago                                                      │
│                                                                     │
│  ─── Yesterday ─────────────────────────────────────────────────  │
│                                                                     │
│  RSA Animation                                                      │
│     Yesterday, 3:45 PM                                              │
│                                                                     │
│  ─── Older ──────────────────────────────────────────────────────  │
│                                                                     │
│  React Reconciler                                                   │
│     Aug 2, 2026                                                     │
│                                                                     │
│  Git Branching                                                      │
│     Aug 1, 2026                                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Features:**
- Search bar (searches conversation titles and messages)
- New conversation button
- Grouped by: Pinned | Today | Yesterday | Older
- Each item shows: title, timestamp
- Right-click context menu: Rename, Duplicate, Archive, Delete, Pin

### 7.5 Conversation Actions

| Action | Description |
|--------|-------------|
| Rename | Edit conversation title |
| Duplicate | Create a copy of the conversation |
| Archive | Move to archive (hidden from main list) |
| Delete | Remove permanently (with confirmation) |
| Pin | Add to pinned section at top |

### 7.6 Settings Drawer (Right Panel)

**Quick settings for common adjustments — not a full page.**

```
┌─────────────────────────────────────────────────────────────────────┐
│  RIGHT PANEL (300px)                                                │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  Generation Settings                                                │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  Model                                                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Vibe Video (Hyperframes)                               [▼]  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Duration                                                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  10s  |  15s  |  [30s]  |  45s  |  60s                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Resolution                                                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  720p  |  [1080p]  |  1440p  |  4K                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  FPS                                                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  24  |  [30]  |  60                                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Aspect Ratio                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  [16:9]  |  9:16  |  1:1  |  4:3  |  21:9                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Style Presets                                                      │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  [Cinematic] [Anime] [Documentary] [Nature] [Product Ads]          │
│  [Motion Graphics] [Logo Reveal] [Social Media]                    │
│                                                                     │
│  Advanced Options                                                   │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│  Seed                                                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  [Random ✓]  or  [____________]                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ☐ Strict mode (follow prompt exactly)                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 8. Responsive Strategy

### 8.1 Desktop (≥1280px)

- Full three-panel layout
- Left panel: 280px
- Center panel: flex: 1
- Right panel: 300px
- All features visible
- Prompt dock fixed at bottom

### 8.2 Laptop (1024px - 1279px)

- Three-panel layout
- Left panel: 240px
- Right panel: 280px
- Slightly compressed
- All features visible

### 8.3 Tablet (768px - 1023px)

- Two-panel layout (left + center)
- Right panel: Hidden (accessible via settings icon)
- Left panel: 200px or icon-only
- Center panel: remaining width
- Touch-optimized tap targets (min 44px)

### 8.4 Mobile (< 768px)

- Single panel (center only)
- Left panel: Hidden (hamburger menu)
- Right panel: Hidden (settings icon opens drawer)
- Bottom navigation bar:
  ```
  ┌────────────────────────────────┐
  │  [Create]  [History]  [Settings]│
  └────────────────────────────────┘
  ```
- Larger tap targets (min 48px)
- Simplified animations
- Prompt dock remains at bottom

### 8.5 Breakpoint System

```css
/* Tailwind breakpoints */
sm: 640px    /* Large phones */
md: 768px    /* Tablets */
lg: 1024px   /* Small laptops */
xl: 1280px   /* Desktops */
2xl: 1536px  /* Large screens */
```

### 8.6 Responsive Patterns

| Element | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| Left panel | 280px | 200px | Hidden (drawer) |
| Center panel | flex: 1 | flex: 1 | Full width |
| Right panel | 300px | Hidden (icon) | Hidden (drawer) |
| Video grid | 3-4 columns | 2 columns | 1 column |
| Prompt dock | Fixed bottom | Fixed bottom | Fixed bottom |
| Navigation | Top bar | Top bar | Bottom bar |
| Video preview | Inline (HERO) | Inline (HERO) | Full width |

---

## 9. Design System

### 9.1 Color Palette

**Primary:**
| Name | Hex | Tailwind |
|------|-----|----------|
| Background | #09090b | zinc-950 |
| Surface | #18181b | zinc-900 |
| Elevated | #27272a | zinc-800 |
| Active | #3f3f46 | zinc-700 |

**Accent:**
| Name | Hex | Tailwind |
|------|-----|----------|
| Primary | #8b5cf6 | violet-500 |
| Hover | #7c3aed | violet-600 |
| Light | #a78bfa | violet-400 |
| Glow | rgba(139,92,246,0.15) | — |

**Text:**
| Name | Hex | Tailwind |
|------|-----|----------|
| Primary | #fafafa | zinc-50 |
| Secondary | #a1a1aa | zinc-400 |
| Tertiary | #71717a | zinc-500 |
| Disabled | #52525b | zinc-600 |

**Semantic:**
| Name | Hex | Tailwind |
|------|-----|----------|
| Success | #22c55e | green-500 |
| Error | #ef4444 | red-500 |
| Warning | #f59e0b | amber-500 |
| Info | #3b82f6 | blue-500 |

### 9.2 Typography Scale

| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| text-xs | 12px | 400 | 16px | Timestamps, meta |
| text-sm | 14px | 400 | 20px | Small text, labels |
| text-base | 16px | 400 | 24px | Body text |
| text-lg | 18px | 400 | 28px | Large body |
| text-xl | 20px | 500 | 28px | Card titles |
| text-2xl | 24px | 600 | 32px | Section headers |
| text-3xl | 30px | 600 | 36px | Page titles |
| text-4xl | 36px | 700 | 40px | Hero titles |
| text-5xl | 48px | 700 | 48px | Landing hero |

### 9.3 Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| rounded-sm | 4px | Badges, tags |
| rounded | 6px | Buttons, inputs |
| rounded-lg | 8px | Buttons, small cards |
| rounded-xl | 12px | Cards, modals |
| rounded-2xl | 16px | Large modals, video player |
| rounded-full | 9999px | Avatars, icons |

### 9.4 Shadows

**Dark theme shadows (rgba(0,0,0)):**

| Token | Value | Usage |
|-------|-------|-------|
| shadow-sm | 0 1px 2px rgba(0,0,0,0.3) | Subtle lift |
| shadow | 0 2px 4px rgba(0,0,0,0.4) | Cards |
| shadow-md | 0 4px 8px rgba(0,0,0,0.5) | Dropdowns |
| shadow-lg | 0 8px 16px rgba(0,0,0,0.6) | Modals |
| shadow-glow | 0 0 20px rgba(139,92,246,0.15) | Accent glow |

### 9.5 Grid System

**12-column grid:**
```css
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 16px;
}
```

**Column spans:**
- Full width: `col-span-12`
- Half width: `col-span-6`
- Third width: `col-span-4`
- Quarter width: `col-span-3`

### 9.6 Spacing Scale

| Token | Value | Tailwind |
|-------|-------|----------|
| space-0 | 0px | p-0 / m-0 |
| space-1 | 4px | p-1 / m-1 |
| space-2 | 8px | p-2 / m-2 |
| space-3 | 12px | p-3 / m-3 |
| space-4 | 16px | p-4 / m-4 |
| space-5 | 20px | p-5 / m-5 |
| space-6 | 24px | p-6 / m-6 |
| space-8 | 32px | p-8 / m-8 |
| space-10 | 40px | p-10 / m-10 |
| space-12 | 48px | p-12 / m-12 |
| space-16 | 64px | p-16 / m-16 |
| space-20 | 80px | p-20 / m-20 |
| space-24 | 96px | p-24 / m-24 |

### 9.7 Component Variants

**Button variants:**
- `primary` — Violet bg, white text
- `secondary` — Transparent bg, border, white text
- `ghost` — Transparent bg, no border, gray text
- `danger` — Red bg, white text
- `link` — No bg, underline, accent text

**Button sizes:**
- `sm` — 32px height, 12px padding, 14px font
- `md` — 40px height, 16px padding, 14px font
- `lg` — 48px height, 24px padding, 16px font

**Card variants:**
- `default` — bg-secondary, border
- `glass` — bg-secondary/80, backdrop-blur
- `elevated` — bg-tertiary, shadow-md
- `interactive` — default + hover effects
- `hero` — bg-primary, larger padding, border

### 9.8 Icon Usage

**Icon library:** Lucide Icons (CDN SVG sprite)

**Sizes:**
- `sm` — 16px (inline with text)
- `md` — 20px (buttons)
- `lg` — 24px (standalone)
- `xl` — 32px (feature icons)

**Rules:**
- Always pair icons with text when possible
- Use consistent icon style (all outline or all filled)
- Icons inherit text color by default
- Use accent color for active/primary icons

### 9.9 Motion Guidelines

**Easing functions:**
```css
ease-out: cubic-bezier(0.4, 0, 0.2, 1)
ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)
ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275)
```

**Duration scale:**
| Token | Value | Usage |
|-------|-------|-------|
| duration-fast | 100ms | Hover states, toggles |
| duration-normal | 150ms | Buttons, small elements |
| duration-slow | 300ms | Page transitions, modals |
| duration-slower | 500ms | Complex animations |

**Animation principles:**
1. Purpose — Every animation has a reason
2. Consistency — Same element, same animation
3. Subtlety — Enhance, don't distract
4. Performance — Use transform/opacity only
5. Accessibility — Respect prefers-reduced-motion

---

## 10. Final Notes

### 10.1 Implementation Priority

**Phase 1 — Core (MVP):**
1. Three-panel workspace layout (left, center, right)
2. Prompt dock (fixed bottom)
3. Video generation flow
4. Video HERO preview
5. Basic settings in right panel
6. Conversation list in left panel

**Phase 2 — Polish:**
7. Generation pipeline visualization
8. Rich video cards
9. History gallery (masonry grid)
10. Search and filter
11. Toast notifications
12. Settings drawer

**Phase 3 — Enhancement:**
13. Conversation persistence
14. Categorized prompt suggestions
15. Style presets
16. Advanced options (seed, strict mode)
17. Keyboard shortcuts
18. Drag-and-drop file upload
19. Embed code generation
20. Dark/light theme toggle

### 10.2 API Integration Points

| Endpoint | Method | Usage |
|----------|--------|-------|
| `GET /` | GET | Health check |
| `GET /teams` | GET | List available teams |
| `POST /teams/{id}/runs` | POST | Generate video |
| `GET /teams/{id}/runs/{run_id}` | GET | Get run status |

**Request format:**
```
POST /teams/vibe_video/runs
Content-Type: application/x-www-form-urlencoded

message=Animate+Dijkstra%27s+algorithm&stream=true
```

### 10.3 Performance Budget

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.5s |
| Largest Contentful Paint | < 2.5s |
| Time to Interactive | < 3s |
| Cumulative Layout Shift | < 0.1 |
| Total bundle size | < 100KB (excluding CDN) |

### 10.4 Browser Support

| Browser | Version |
|---------|---------|
| Chrome | Latest 2 versions |
| Firefox | Latest 2 versions |
| Safari | Latest 2 versions |
| Edge | Latest 2 versions |

### 10.5 Accessibility Checklist

- [ ] WCAG AA contrast ratios (4.5:1 text, 3:1 large text)
- [ ] Keyboard navigation for all interactive elements
- [ ] Focus visible rings on all focusable elements
- [ ] ARIA labels on all buttons and inputs
- [ ] Skip to main content link
- [ ] Alt text on all images and video thumbnails
- [ ] prefers-reduced-motion support
- [ ] Screen reader testing
- [ ] Touch target minimum 44px on mobile

### 10.6 Design Philosophy Summary

The application should feel like a **world-class AI Creative Studio** — not a chatbot. Key principles:

1. **Video is hero** — Generated videos are always the visual focal point
2. **Professional workspace** — Three-panel layout, not chat interface
3. **Premium dark theme** — Midjourney-inspired, immersive
4. **Minimal distractions** — Clean, spacious, focused
5. **Strong visual hierarchy** — Video > Prompt > Settings > Navigation
6. **Elegant micro-interactions** — Enhance workflow, not distract
7. **Consistent design system** — Tokens, components, patterns
8. **High-quality animations** — Smooth, purposeful, accessible
9. **Accessibility first** — WCAG compliant, keyboard navigable
10. **Responsive excellence** — Desktop-first, mobile-optimized

---

**End of Planning Document**

*Version 2.0 — AI Creative Studio Edition*
*This document is a blueprint for implementation. No code has been written. Another AI or developer can use this document to build the entire interface using Tailwind CSS CDN and Vanilla JavaScript while maintaining a premium, production-quality user experience.*
