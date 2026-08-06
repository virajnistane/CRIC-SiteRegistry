{{/*
Expand the name of the chart.
*/}}
{{- define "cric-site-registry.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "cric-site-registry.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "cric-site-registry.labels" -}}
helm.sh/chart: {{ include "cric-site-registry.chart" . }}
{{ include "cric-site-registry.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "cric-site-registry.selectorLabels" -}}
app.kubernetes.io/name: {{ include "cric-site-registry.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Chart name and version, used in labels.
*/}}
{{- define "cric-site-registry.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Postgres service host, e.g. release-cric-site-registry-postgres
*/}}
{{- define "cric-site-registry.postgresHost" -}}
{{- printf "%s-postgres" (include "cric-site-registry.fullname" .) }}
{{- end }}
