const BAKU_ORDER_KEY = 'bakuLeadOrder';

const PACKAGE_CATALOG = {
    starter_saas: {
        id: 'starter_saas',
        name: 'Starter SaaS',
        industry: 'SaaS',
        tier: 'Estandar',
        tierId: 'standard',
        exclusivity: 'Compartido',
        exclusivityId: 'shared',
        leadCount: 250,
        basePrice: 297,
        description: '250 leads B2B del sector SaaS con nombre, email y empresa verificados.',
        includes: [
            'Nombre, empresa y correo corporativo verificado.',
            'Cargo, pais y tamano estimado de compania.',
            'Base limpia para CRM y outreach inicial.',
            'Validacion estandar de entregabilidad.'
        ]
    },
    growth_tech: {
        id: 'growth_tech',
        name: 'Growth Tech',
        industry: 'Tecnologia',
        tier: 'Premium',
        tierId: 'premium',
        exclusivity: 'Exclusivo',
        exclusivityId: 'exclusive',
        leadCount: 500,
        basePrice: 697,
        description: '500 leads de tecnologia enriquecidos con LinkedIn, telefono y senales de intencion.',
        includes: [
            'LinkedIn y telefono directo cuando aplica.',
            'Senales de intencion y dominio de empresa.',
            'Mayor contexto para outreach consultivo.',
            'Reservado para un solo cliente.'
        ]
    },
    enterprise_pack: {
        id: 'enterprise_pack',
        name: 'Enterprise Pack',
        industry: 'Multi-industria',
        tier: 'Enterprise',
        tierId: 'enterprise',
        exclusivity: 'Exclusivo',
        exclusivityId: 'exclusive',
        leadCount: 1000,
        basePrice: 1497,
        description: '1,000 leads multi-industria con datos completos: tecnografia, org chart y trigger events.',
        includes: [
            'Todo Growth, mas tecnografia y org chart parcial.',
            'Trigger events recientes y scoring de cuentas.',
            'Mayor profundidad para equipos de venta complejos.',
            'Soporte dedicado para definir criterios.'
        ]
    },
    retail_essentials: {
        id: 'retail_essentials',
        name: 'Retail Essentials',
        industry: 'Retail',
        tier: 'Estandar',
        tierId: 'standard',
        exclusivity: 'Compartido',
        exclusivityId: 'shared',
        leadCount: 300,
        basePrice: 347,
        description: '300 leads del sector retail con datos basicos verificados.',
        includes: [
            'Base comercial limpia para activacion rapida.',
            'Leads verificados con estructura estandar.',
            'Buen fit para campanas de volumen controlado.',
            'Entrega lista para secuencias o CRM.'
        ]
    },
    real_estate_pro: {
        id: 'real_estate_pro',
        name: 'Real Estate Pro',
        industry: 'Real Estate',
        tier: 'Premium',
        tierId: 'premium',
        exclusivity: 'Exclusivo',
        exclusivityId: 'exclusive',
        leadCount: 400,
        basePrice: 597,
        description: '400 leads inmobiliarios enriquecidos con datos de contacto completos.',
        includes: [
            'Contacto directo verificado y LinkedIn.',
            'Telefono directo y senales de oportunidad.',
            'Contexto para venta consultiva sectorial.',
            'Exclusividad para proteger territorio comercial.'
        ]
    },
    fintech_growth: {
        id: 'fintech_growth',
        name: 'Fintech Growth',
        industry: 'Fintech',
        tier: 'Premium',
        tierId: 'premium',
        exclusivity: 'Compartido',
        exclusivityId: 'shared',
        leadCount: 500,
        basePrice: 797,
        description: '500 leads fintech con LinkedIn, telefono y senales de intencion.',
        includes: [
            'Decision makers verificados y contexto de cuenta.',
            'LinkedIn, telefono y senales de intencion.',
            'Ideal para campanas de captacion outbound.',
            'Segmentacion optimizada para minimizar solapamientos.'
        ]
    }
};

const OBJECTIVES = {
    pipeline: 'Generar pipeline nuevo',
    abm: 'Campana ABM o named accounts',
    territory: 'Abrir nueva geografia',
    enterprise: 'Prospeccion enterprise',
    partnerships: 'Partners, canales o aliados'
};

const FIELD_LABELS = {
    regions: {
        latam: 'LATAM',
        north_america: 'North America',
        europe: 'Europa',
        middle_east: 'Middle East',
        remote: 'Global / remoto'
    },
    companySizes: {
        smb: '1-50 empleados',
        midmarket: '51-200 empleados',
        upper_midmarket: '201-1000 empleados',
        enterprise: '1000+ empleados'
    },
    revenueBands: {
        early: 'Pre-seed a Series A',
        growth: 'Series B-C',
        mature: 'Scale-up / profitable',
        public: 'Publicas o corporates'
    },
    jobLevels: {
        founder: 'Founder / C-Level',
        vp: 'VP / Head',
        director: 'Director',
        manager: 'Manager',
        icp_specialist: 'Specialist / practitioner'
    },
    departments: {
        sales: 'Sales',
        marketing: 'Marketing',
        revenue_ops: 'Revenue Ops',
        partnerships: 'Partnerships',
        product: 'Product',
        finance: 'Finance'
    },
    intentSignals: {
        hiring: 'Hiring activo',
        new_funding: 'Funding reciente',
        tech_change: 'Cambio de stack',
        expansion: 'Expansion geografica',
        outbound_ready: 'Equipo outbound activo'
    },
    requiredFields: {
        work_email: 'Work email verificado',
        linkedin: 'LinkedIn',
        direct_dial: 'Telefono directo',
        intent: 'Senales de intencion',
        company_domain: 'Dominio de empresa',
        technologies: 'Tecnografia',
        org_chart: 'Org chart level'
    },
    addOns: {
        direct_dials_plus: 'Refuerzo de telefonos directos',
        intent_boost: 'Capa extra de intent signals',
        technographics_plus: 'Technographics detallado',
        crm_mapping: 'Mapeo para CRM',
        scoring: 'Scoring custom de cuentas',
        suppression_review: 'Dedupe y suppression review'
    }
};

const TURNAROUND_OPTIONS = {
    standard: { label: 'Plazo normal', note: '3 a 5 dias habiles', price: 0 },
    priority: { label: 'Prioridad', note: '48 a 72 horas', price: 149 },
    rush: { label: 'Rush', note: '24 a 48 horas', price: 299 }
};

const OUTPUT_OPTIONS = {
    csv: 'CSV listo para cargar',
    sheets: 'Google Sheets compartido',
    hubspot: 'Plantilla HubSpot',
    salesforce: 'Plantilla Salesforce',
    json: 'JSON / webhook'
};

const ADD_ON_PRICES = {
    direct_dials_plus: 129,
    intent_boost: 229,
    technographics_plus: 179,
    crm_mapping: 99,
    scoring: 159,
    suppression_review: 89
};

function formatUSD(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0
    }).format(amount || 0);
}

function readStoredOrder() {
    try {
        return JSON.parse(window.localStorage.getItem(BAKU_ORDER_KEY) || 'null');
    } catch (error) {
        return null;
    }
}

function saveOrder(order) {
    window.localStorage.setItem(BAKU_ORDER_KEY, JSON.stringify(order));
}

function getPackage(packageId) {
    return PACKAGE_CATALOG[packageId] || PACKAGE_CATALOG.growth_tech;
}

function getSelectedValues(formData, name) {
    return formData.getAll(name).filter(Boolean);
}

function defaultCustomization(pkg) {
    return {
        campaignName: `${pkg.name} - custom brief`,
        teamName: '',
        objective: 'pipeline',
        regions: pkg.industry === 'Multi-industria' ? ['latam', 'north_america'] : ['latam'],
        countries: '',
        cities: '',
        subVerticals: pkg.industry,
        companySizes: pkg.tierId === 'enterprise' ? ['upper_midmarket', 'enterprise'] : ['midmarket'],
        revenueBands: pkg.tierId === 'enterprise' ? ['growth', 'mature'] : ['growth'],
        jobLevels: pkg.tierId === 'standard' ? ['manager', 'director'] : ['director', 'vp'],
        departments: ['sales', 'marketing'],
        titleKeywords: '',
        technologyKeywords: '',
        namedAccounts: '',
        exclusions: '',
        intentSignals: pkg.tierId === 'standard' ? ['hiring'] : ['hiring', 'new_funding'],
        requiredFields: pkg.tierId === 'standard'
            ? ['work_email', 'company_domain']
            : pkg.tierId === 'premium'
                ? ['work_email', 'linkedin', 'direct_dial', 'intent']
                : ['work_email', 'linkedin', 'direct_dial', 'intent', 'technologies', 'org_chart'],
        addOns: [],
        leadCountExtra: 0,
        turnaround: 'standard',
        outputFormat: 'csv',
        crmSync: 'none',
        exclusivityChoice: pkg.exclusivityId,
        freshnessWindow: '90',
        dedupeAgainstCrm: 'yes',
        notes: ''
    };
}

function getOrderFromPackage(packageId) {
    const pkg = getPackage(packageId);
    return {
        packageId: pkg.id,
        createdAt: new Date().toISOString(),
        customization: defaultCustomization(pkg)
    };
}

function mergeWithStored(packageId) {
    const stored = readStoredOrder();
    if (stored && stored.packageId === packageId && stored.customization) {
        return {
            packageId,
            createdAt: stored.createdAt || new Date().toISOString(),
            customization: {
                ...defaultCustomization(getPackage(packageId)),
                ...stored.customization
            }
        };
    }

    return getOrderFromPackage(packageId);
}

function getExtraLeadPrice(pkg, extraLeadCount) {
    const extra = Number(extraLeadCount || 0);
    if (!extra) return 0;
    const unitCost = pkg.basePrice / pkg.leadCount;
    return Math.round(unitCost * extra * 0.82);
}

function buildPricing(order) {
    const pkg = getPackage(order.packageId);
    const custom = order.customization || {};
    const turnaround = TURNAROUND_OPTIONS[custom.turnaround] || TURNAROUND_OPTIONS.standard;
    const extraLeadPrice = getExtraLeadPrice(pkg, custom.leadCountExtra);
    const exclusivityUpgrade = custom.exclusivityChoice === 'exclusive' && pkg.exclusivityId === 'shared'
        ? Math.round(pkg.basePrice * 0.35)
        : 0;
    const addOns = (custom.addOns || []).map((id) => ({
        id,
        label: FIELD_LABELS.addOns[id],
        price: ADD_ON_PRICES[id] || 0
    }));
    const addOnTotal = addOns.reduce((sum, item) => sum + item.price, 0);
    const total = pkg.basePrice + extraLeadPrice + turnaround.price + exclusivityUpgrade + addOnTotal;

    return {
        base: pkg.basePrice,
        extraLeadPrice,
        turnaround,
        exclusivityUpgrade,
        addOns,
        addOnTotal,
        totalLeadCount: pkg.leadCount + Number(custom.leadCountExtra || 0),
        total
    };
}

function listFromDictionary(dictionary, selectedValues) {
    return (selectedValues || []).map((value) => dictionary[value]).filter(Boolean);
}

function textOrFallback(value, fallback) {
    return value && String(value).trim() ? value.trim() : fallback;
}

function joinReadable(values, fallback) {
    if (!values || values.length === 0) return fallback;
    return values.join(', ');
}

function formatCrmSync(value) {
    const crmValue = textOrFallback(value, 'none');
    if (crmValue === 'none') return 'Sin stack especifico';
    if (crmValue === 'hubspot') return 'HubSpot';
    if (crmValue === 'salesforce') return 'Salesforce';
    if (crmValue === 'pipedrive') return 'Pipedrive';
    if (crmValue === 'apollo') return 'Apollo';
    return crmValue;
}

function hydrateForm(form, order) {
    const custom = order.customization;

    Object.entries(custom).forEach(([key, value]) => {
        if (Array.isArray(value)) {
            value.forEach((item) => {
                const input = form.querySelector(`[name="${key}"][value="${item}"]`);
                if (input) input.checked = true;
            });
            return;
        }

        const input = form.querySelector(`[name="${key}"]`);
        if (!input) return;

        if (input.type === 'radio') {
            const radio = form.querySelector(`[name="${key}"][value="${value}"]`);
            if (radio) radio.checked = true;
        } else {
            input.value = value;
        }
    });
}

function collectOrderFromForm(form, packageId) {
    const formData = new FormData(form);
    const pkg = getPackage(packageId);
    const exclusivityChoice = pkg.exclusivityId === 'exclusive'
        ? 'exclusive'
        : formData.get('exclusivityChoice') || 'shared';

    return {
        packageId,
        createdAt: new Date().toISOString(),
        customization: {
            campaignName: formData.get('campaignName') || `${pkg.name} - custom brief`,
            teamName: formData.get('teamName') || '',
            objective: formData.get('objective') || 'pipeline',
            regions: getSelectedValues(formData, 'regions'),
            countries: formData.get('countries') || '',
            cities: formData.get('cities') || '',
            subVerticals: formData.get('subVerticals') || '',
            companySizes: getSelectedValues(formData, 'companySizes'),
            revenueBands: getSelectedValues(formData, 'revenueBands'),
            jobLevels: getSelectedValues(formData, 'jobLevels'),
            departments: getSelectedValues(formData, 'departments'),
            titleKeywords: formData.get('titleKeywords') || '',
            technologyKeywords: formData.get('technologyKeywords') || '',
            namedAccounts: formData.get('namedAccounts') || '',
            exclusions: formData.get('exclusions') || '',
            intentSignals: getSelectedValues(formData, 'intentSignals'),
            requiredFields: getSelectedValues(formData, 'requiredFields'),
            addOns: getSelectedValues(formData, 'addOns'),
            leadCountExtra: Number(formData.get('leadCountExtra') || 0),
            turnaround: formData.get('turnaround') || 'standard',
            outputFormat: formData.get('outputFormat') || 'csv',
            crmSync: formData.get('crmSync') || 'none',
            exclusivityChoice,
            freshnessWindow: formData.get('freshnessWindow') || '90',
            dedupeAgainstCrm: formData.get('dedupeAgainstCrm') || 'yes',
            notes: formData.get('notes') || ''
        }
    };
}

function fillText(id, value) {
    const node = document.getElementById(id);
    if (node) node.textContent = value;
}

function fillHTML(id, value) {
    const node = document.getElementById(id);
    if (node) node.innerHTML = value;
}

function renderPackageMeta(pkg) {
    return `${pkg.industry} / ${pkg.tier} / ${pkg.leadCount} leads base`;
}

function renderPriceTable(target, rows, total) {
    if (!target) return;
    target.innerHTML = rows.map((row) => `
        <div class="price-row${row.muted ? ' muted' : ''}">
            <span>${row.label}</span>
            <strong>${row.value}</strong>
        </div>
    `).join('') + `
        <div class="price-row total">
            <span>Total estimado</span>
            <strong>${formatUSD(total)}</strong>
        </div>
    `;
}

function buildSummaryRows(order) {
    const pkg = getPackage(order.packageId);
    const custom = order.customization;
    const pricing = buildPricing(order);
    const addOnLabel = pricing.addOns.length
        ? joinReadable(pricing.addOns.map((item) => item.label), 'Sin add-ons')
        : 'Sin add-ons';

    return {
        targeting: [
            {
                key: 'Objetivo',
                value: OBJECTIVES[custom.objective] || 'Generar pipeline nuevo'
            },
            {
                key: 'Geografia',
                value: joinReadable(listFromDictionary(FIELD_LABELS.regions, custom.regions), 'No definida')
            },
            {
                key: 'Tamano empresa',
                value: joinReadable(listFromDictionary(FIELD_LABELS.companySizes, custom.companySizes), 'Sin restriccion')
            },
            {
                key: 'Seniority',
                value: joinReadable(listFromDictionary(FIELD_LABELS.jobLevels, custom.jobLevels), 'No definido')
            },
            {
                key: 'Departamentos',
                value: joinReadable(listFromDictionary(FIELD_LABELS.departments, custom.departments), 'No definido')
            },
            {
                key: 'Titulos / keywords',
                value: textOrFallback(custom.titleKeywords, 'Sin keywords especificas')
            }
        ],
        ops: [
            {
                key: 'Volumen final',
                value: `${pricing.totalLeadCount} leads`
            },
            {
                key: 'Exclusividad',
                value: custom.exclusivityChoice === 'exclusive' ? 'Exclusivo' : 'Compartido'
            },
            {
                key: 'Entrega',
                value: OUTPUT_OPTIONS[custom.outputFormat] || 'CSV listo para cargar'
            },
            {
                key: 'Turnaround',
                value: `${TURNAROUND_OPTIONS[custom.turnaround].label} / ${TURNAROUND_OPTIONS[custom.turnaround].note}`
            },
            {
                key: 'CRM sync',
                value: formatCrmSync(custom.crmSync)
            },
            {
                key: 'Add-ons',
                value: addOnLabel
            }
        ],
        pricingRows: [
            { label: `${pkg.name} base`, value: formatUSD(pricing.base) },
            { label: `Leads extra (${custom.leadCountExtra || 0})`, value: formatUSD(pricing.extraLeadPrice), muted: !pricing.extraLeadPrice },
            { label: `Turnaround`, value: formatUSD(pricing.turnaround.price), muted: !pricing.turnaround.price },
            { label: `Upgrade exclusividad`, value: formatUSD(pricing.exclusivityUpgrade), muted: !pricing.exclusivityUpgrade },
            { label: `Add-ons`, value: formatUSD(pricing.addOnTotal), muted: !pricing.addOnTotal }
        ],
        pricing
    };
}

function renderCustomizeSummary(order) {
    const pkg = getPackage(order.packageId);
    const custom = order.customization;
    const summary = buildSummaryRows(order);
    const targetingPills = [
        ...(listFromDictionary(FIELD_LABELS.regions, custom.regions)),
        ...(listFromDictionary(FIELD_LABELS.departments, custom.departments)),
        ...(listFromDictionary(FIELD_LABELS.jobLevels, custom.jobLevels))
    ].slice(0, 8);
    const fieldPills = listFromDictionary(FIELD_LABELS.requiredFields, custom.requiredFields).slice(0, 8);

    fillText('summary-package-tag', `${pkg.tier} / ${pkg.exclusivity}`);
    fillText('summary-package-name', pkg.name);
    fillText('summary-package-copy', pkg.description);
    fillHTML('summary-targeting-pills', targetingPills.length
        ? targetingPills.map((item) => `<span class="summary-pill">${item}</span>`).join('')
        : '<span class="summary-pill">Definir segmentacion</span>');
    fillHTML('summary-field-pills', fieldPills.length
        ? fieldPills.map((item) => `<span class="summary-pill">${item}</span>`).join('')
        : '<span class="summary-pill">Campos base</span>');
    renderPriceTable(document.getElementById('summary-pricing'), summary.pricingRows, summary.pricing.total);
    fillText('summary-volume', `${summary.pricing.totalLeadCount} leads`);
    fillText('summary-turnaround', TURNAROUND_OPTIONS[custom.turnaround].note);
}

function setPackageContent(pkg) {
    fillText('selected-package-name', pkg.name);
    fillText('selected-package-meta', renderPackageMeta(pkg));
    fillText('selected-package-copy', pkg.description);
    fillText('selected-package-price', formatUSD(pkg.basePrice));
    fillText('selected-package-count', `${pkg.leadCount} leads base`);
    fillHTML('selected-package-includes', pkg.includes.map((item) => `<li>${item}</li>`).join(''));
}

function toggleExclusiveUpgrade(pkg) {
    const upgradeBlock = document.getElementById('exclusive-upgrade-block');
    const lockedNote = document.getElementById('exclusive-locked-note');
    if (!upgradeBlock || !lockedNote) return;

    if (pkg.exclusivityId === 'exclusive') {
        upgradeBlock.style.display = 'none';
        lockedNote.style.display = 'block';
    } else {
        upgradeBlock.style.display = 'grid';
        lockedNote.style.display = 'none';
    }
}

function initCustomizePage() {
    const form = document.getElementById('customize-form');
    if (!form) return;

    const params = new URLSearchParams(window.location.search);
    const packageId = params.get('package') || readStoredOrder()?.packageId || 'growth_tech';
    const pkg = getPackage(packageId);
    const order = mergeWithStored(pkg.id);

    setPackageContent(pkg);
    toggleExclusiveUpgrade(pkg);
    hydrateForm(form, order);
    renderCustomizeSummary(order);

    form.addEventListener('input', () => {
        renderCustomizeSummary(collectOrderFromForm(form, pkg.id));
    });

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const nextOrder = collectOrderFromForm(form, pkg.id);
        saveOrder(nextOrder);
        window.location.href = '/cart.html';
    });

    const resetButton = document.getElementById('reset-brief');
    if (resetButton) {
        resetButton.addEventListener('click', () => {
            const fresh = getOrderFromPackage(pkg.id);
            form.reset();
            hydrateForm(form, fresh);
            renderCustomizeSummary(fresh);
        });
    }
}

function renderDetailList(targetId, rows) {
    const target = document.getElementById(targetId);
    if (!target) return;
    target.innerHTML = rows.map((row) => `
        <div class="detail-row">
            <div class="detail-key">${row.key}</div>
            <div class="detail-value">${row.value}</div>
        </div>
    `).join('');
}

function initCartPage() {
    const emptyState = document.getElementById('cart-empty');
    const content = document.getElementById('cart-content');
    const order = readStoredOrder();

    if (!order) {
        if (emptyState) emptyState.style.display = 'block';
        if (content) content.style.display = 'none';
        return;
    }

    const pkg = getPackage(order.packageId);
    const custom = order.customization;
    const summary = buildSummaryRows(order);

    fillText('cart-package-name', pkg.name);
    fillText('cart-package-meta', renderPackageMeta(pkg));
    fillText('cart-package-copy', pkg.description);
    fillText('cart-total', formatUSD(summary.pricing.total));
    fillText('cart-count', `${summary.pricing.totalLeadCount} leads`);
    fillText('cart-turnaround', TURNAROUND_OPTIONS[custom.turnaround].note);
    fillHTML('cart-pill-list', [
        pkg.industry,
        custom.exclusivityChoice === 'exclusive' ? 'Exclusivo' : 'Compartido',
        OUTPUT_OPTIONS[custom.outputFormat],
        `${summary.pricing.totalLeadCount} leads`
    ].map((item) => `<span class="summary-pill">${item}</span>`).join(''));

    renderDetailList('cart-targeting-details', [
        { key: 'Objetivo', value: OBJECTIVES[custom.objective] || 'Generar pipeline nuevo' },
        { key: 'Regiones', value: joinReadable(listFromDictionary(FIELD_LABELS.regions, custom.regions), 'No definidas') },
        { key: 'Paises / ciudades', value: joinReadable([textOrFallback(custom.countries, ''), textOrFallback(custom.cities, '')].filter(Boolean), 'Sin filtro adicional') },
        { key: 'Subverticales', value: textOrFallback(custom.subVerticals, pkg.industry) },
        { key: 'Tamano y revenue', value: joinReadable([
            joinReadable(listFromDictionary(FIELD_LABELS.companySizes, custom.companySizes), ''),
            joinReadable(listFromDictionary(FIELD_LABELS.revenueBands, custom.revenueBands), '')
        ].filter(Boolean), 'Sin restriccion') },
        { key: 'Roles objetivo', value: joinReadable([
            joinReadable(listFromDictionary(FIELD_LABELS.departments, custom.departments), ''),
            joinReadable(listFromDictionary(FIELD_LABELS.jobLevels, custom.jobLevels), ''),
            textOrFallback(custom.titleKeywords, '')
        ].filter(Boolean), 'No definidos') },
        { key: 'Tecnologias / senales', value: joinReadable([
            textOrFallback(custom.technologyKeywords, ''),
            joinReadable(listFromDictionary(FIELD_LABELS.intentSignals, custom.intentSignals), '')
        ].filter(Boolean), 'Sin restricciones') },
        { key: 'Exclusiones', value: textOrFallback(custom.exclusions, 'Sin exclusiones cargadas') }
    ]);

    renderDetailList('cart-ops-details', [
        { key: 'Campos requeridos', value: joinReadable(listFromDictionary(FIELD_LABELS.requiredFields, custom.requiredFields), 'Campos base') },
        { key: 'Add-ons', value: summary.pricing.addOns.length ? joinReadable(summary.pricing.addOns.map((item) => item.label), 'Sin add-ons') : 'Sin add-ons' },
        { key: 'Dedupe contra CRM', value: custom.dedupeAgainstCrm === 'yes' ? 'Si, deduplicar contra base existente' : 'No, entregar universo completo' },
        { key: 'CRM / entrega', value: joinReadable([OUTPUT_OPTIONS[custom.outputFormat], formatCrmSync(custom.crmSync)].filter(Boolean), 'CSV') },
        { key: 'Freshness window', value: `${custom.freshnessWindow} dias` },
        { key: 'Notas especiales', value: textOrFallback(custom.notes, 'Sin notas adicionales') }
    ]);

    renderPriceTable(document.getElementById('cart-pricing'), summary.pricingRows, summary.pricing.total);

    const editLink = document.getElementById('edit-customization');
    if (editLink) {
        editLink.href = `/customize.html?package=${pkg.id}`;
    }
}

function initPaymentPage() {
    const emptyState = document.getElementById('payment-empty');
    const content = document.getElementById('payment-content');
    const order = readStoredOrder();

    if (!order) {
        if (emptyState) emptyState.style.display = 'block';
        if (content) content.style.display = 'none';
        return;
    }

    const pkg = getPackage(order.packageId);
    const summary = buildSummaryRows(order);
    fillText('payment-package-name', pkg.name);
    fillText('payment-package-meta', renderPackageMeta(pkg));
    fillText('payment-total', formatUSD(summary.total));
    fillText('payment-volume', `${summary.totalLeadCount} leads`);
    renderPriceTable(document.getElementById('payment-pricing'), buildSummaryRows(order).pricingRows, summary.total);

    const form = document.getElementById('payment-form');
    const successState = document.getElementById('payment-success');
    const payButton = document.getElementById('submit-payment');

    if (!form) return;

    form.addEventListener('change', () => {
        const method = form.querySelector('input[name="paymentMethod"]:checked')?.value || 'card';
        if (!payButton) return;
        payButton.textContent = method === 'invoice'
            ? 'Solicitar invoice y confirmar pedido'
            : method === 'wire'
                ? 'Reservar pedido y recibir instrucciones'
                : 'Pagar y confirmar pedido';
    });

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const method = formData.get('paymentMethod') || 'card';
        const orderCode = `BK-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
        fillText('success-order-code', orderCode);
        fillText('success-order-total', formatUSD(summary.total));
        fillText('success-contact-email', String(formData.get('email') || 'tu correo'));
        fillText('success-payment-method', method === 'invoice' ? 'invoice' : method === 'wire' ? 'transferencia' : 'tarjeta');
        if (successState) successState.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const page = document.body.dataset.page;
    if (page === 'customize') initCustomizePage();
    if (page === 'cart') initCartPage();
    if (page === 'payment') initPaymentPage();
});
