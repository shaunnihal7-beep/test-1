import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Checkbox } from './ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { ChevronDown, ChevronUp } from 'lucide-react';

const QuestionnaireSection = ({ 
  section, 
  isExpanded, 
  onToggle, 
  completion, 
  formData, 
  updateFormData 
}) => {
  const renderField = (field) => {
    const value = formData[field.id] || '';

    switch (field.type) {
      case 'text':
        return (
          <div key={field.id} className="space-y-2">
            <Label htmlFor={field.id} className="text-slate-200">
              {field.label} {field.required && <span className="text-red-400">*</span>}
            </Label>
            <Input
              id={field.id}
              value={value}
              onChange={(e) => updateFormData(field.id, e.target.value)}
              placeholder={field.placeholder}
              className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400"
              required={field.required}
            />
            {field.tooltip && (
              <p className="text-xs text-slate-400">{field.tooltip}</p>
            )}
          </div>
        );

      case 'textarea':
        return (
          <div key={field.id} className="space-y-2">
            <Label htmlFor={field.id} className="text-slate-200">
              {field.label} {field.required && <span className="text-red-400">*</span>}
            </Label>
            <Textarea
              id={field.id}
              value={value}
              onChange={(e) => updateFormData(field.id, e.target.value)}
              placeholder={field.placeholder}
              className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 min-h-[100px]"
              required={field.required}
            />
            {field.tooltip && (
              <p className="text-xs text-slate-400">{field.tooltip}</p>
            )}
          </div>
        );

      case 'select':
        return (
          <div key={field.id} className="space-y-2">
            <Label htmlFor={field.id} className="text-slate-200">
              {field.label} {field.required && <span className="text-red-400">*</span>}
            </Label>
            <Select value={value} onValueChange={(val) => updateFormData(field.id, val)}>
              <SelectTrigger className="bg-slate-700/50 border-slate-600 text-white">
                <SelectValue placeholder={field.placeholder} />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-600">
                {field.options?.map((option) => (
                  <SelectItem key={option.value} value={option.value} className="text-white hover:bg-slate-700">
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {field.tooltip && (
              <p className="text-xs text-slate-400">{field.tooltip}</p>
            )}
          </div>
        );

      case 'radio':
        return (
          <div key={field.id} className="space-y-3">
            <Label className="text-slate-200">
              {field.label} {field.required && <span className="text-red-400">*</span>}
            </Label>
            <RadioGroup
              value={value}
              onValueChange={(val) => updateFormData(field.id, val)}
              className="space-y-2"
            >
              {field.options?.map((option) => (
                <div key={option.value} className="flex items-center space-x-2">
                  <RadioGroupItem 
                    value={option.value} 
                    id={`${field.id}-${option.value}`}
                    className="border-slate-500 text-cyan-400"
                  />
                  <Label 
                    htmlFor={`${field.id}-${option.value}`} 
                    className="text-slate-300 cursor-pointer"
                  >
                    {option.label}
                  </Label>
                </div>
              ))}
            </RadioGroup>
            {field.tooltip && (
              <p className="text-xs text-slate-400">{field.tooltip}</p>
            )}
          </div>
        );

      case 'number':
        return (
          <div key={field.id} className="space-y-2">
            <Label htmlFor={field.id} className="text-slate-200">
              {field.label} {field.required && <span className="text-red-400">*</span>}
            </Label>
            <Input
              id={field.id}
              type="number"
              value={value}
              onChange={(e) => updateFormData(field.id, parseFloat(e.target.value) || '')}
              placeholder={field.placeholder}
              min={field.min}
              max={field.max}
              className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400"
              required={field.required}
            />
            {field.tooltip && (
              <p className="text-xs text-slate-400">{field.tooltip}</p>
            )}
          </div>
        );

      case 'email':
        return (
          <div key={field.id} className="space-y-2">
            <Label htmlFor={field.id} className="text-slate-200">
              {field.label} {field.required && <span className="text-red-400">*</span>}
            </Label>
            <Input
              id={field.id}
              type="email"
              value={value}
              onChange={(e) => updateFormData(field.id, e.target.value)}
              placeholder={field.placeholder}
              className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400"
              required={field.required}
            />
            {field.tooltip && (
              <p className="text-xs text-slate-400">{field.tooltip}</p>
            )}
          </div>
        );

      case 'checkbox':
        return (
          <div key={field.id} className="space-y-3">
            <Label className="text-slate-200">
              {field.label} {field.required && <span className="text-red-400">*</span>}
            </Label>
            <div className="space-y-2">
              {field.options?.map((option) => {
                const isChecked = Array.isArray(value) ? value.includes(option.value) : false;
                return (
                  <div key={option.value} className="flex items-center space-x-2">
                    <Checkbox
                      id={`${field.id}-${option.value}`}
                      checked={isChecked}
                      onCheckedChange={(checked) => {
                        const currentValue = Array.isArray(value) ? value : [];
                        if (checked) {
                          updateFormData(field.id, [...currentValue, option.value]);
                        } else {
                          updateFormData(field.id, currentValue.filter(v => v !== option.value));
                        }
                      }}
                      className="border-slate-500 data-[state=checked]:bg-cyan-600"
                    />
                    <Label 
                      htmlFor={`${field.id}-${option.value}`} 
                      className="text-slate-300 cursor-pointer"
                    >
                      {option.label}
                    </Label>
                  </div>
                );
              })}
            </div>
            {field.tooltip && (
              <p className="text-xs text-slate-400">{field.tooltip}</p>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  const getCompletionColor = (completion) => {
    if (completion === 100) return 'text-green-400';
    if (completion >= 50) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <Card className="bg-slate-800/50 border-slate-700">
      <CardHeader 
        className="cursor-pointer hover:bg-slate-800/70 transition-colors"
        onClick={onToggle}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold text-cyan-400">
                {section.number}
              </span>
              <CardTitle className="text-xl text-white">
                {section.title}
              </CardTitle>
            </div>
            <Badge variant="outline" className={`${getCompletionColor(completion)} border-current`}>
              {completion}%
            </Badge>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-slate-300">
                Weight: {section.weight}%
              </p>
            </div>
            {isExpanded ? (
              <ChevronUp className="h-5 w-5 text-slate-400" />
            ) : (
              <ChevronDown className="h-5 w-5 text-slate-400" />
            )}
          </div>
        </div>
        
        {!isExpanded && (
          <div className="mt-4">
            <Progress value={completion} className="h-2" />
          </div>
        )}
      </CardHeader>
      
      {isExpanded && (
        <CardContent className="space-y-6">
          <div className="mb-4">
            <Progress value={completion} className="h-2" />
          </div>
          
          <p className="text-slate-300 text-sm leading-relaxed">
            {section.description}
          </p>
          
          <div className="grid gap-6">
            {section.fields.map(renderField)}
          </div>
        </CardContent>
      )}
    </Card>
  );
};

export default QuestionnaireSection;